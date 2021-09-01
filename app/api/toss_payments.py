from app import schemas

from typing import Union, Mapping, TypeVar, Optional
from fastapi.encoders import jsonable_encoder
from multidict import CIMultiDict, CIMultiDictProxy, istr

import requests

from app.core.config import settings

Headers = Union[Mapping[Union[str, istr], str], CIMultiDict, CIMultiDictProxy]

BASE_URL = 'https://api.tosspayments.com'


class DepsTossPayments():
    def __init__(self):
        """
        Deps object for Toss Payments API
        """

        self.authorization = settings.TOSS_AUTHORIZATION
        self.headers: Headers = {"Authorization": f"Basic {self.authorization}"}

    def serialize_payment(self, obj_in):
        obj_in_data = jsonable_encoder(obj_in)
        return schemas.Payment(**obj_in_data)

    def encapsulate_payment_for_client(self, obj_in: schemas.Payment):
        obj_dict = obj_in.dict()
        obj_dict["secret"] = None
        return schemas.PaymentClient(**obj_dict)

    def read_payment(self, payment_key: str):
        r = requests.get(url=f"{BASE_URL}/v1/payments/{payment_key}", headers=self.headers)
        return r.json()

    def read_payment_by_order_id(self, order_id: Union[str, int]):
        r = requests.get(url=f"{BASE_URL}/v1/payments/orders/{order_id}", headers=self.headers)
        return r.json()

    def ack_payment(self, payment_key: str, order_id: Union[str, int], amount: int):
        r = requests.post(url=f"{BASE_URL}/v1/payments/{payment_key}",
                          json={"orderId": f"{order_id}", "amount": amount},
                          headers=self.headers)
        return r.json()

    def cancel_payment(self, payment_key: str, cancel_reason: str, refund_receive_account: dict = None):
        if refund_receive_account is None:
            body = {"cancelReason": f"{cancel_reason}", }
        else:
            body = {"cancelReason": f"{cancel_reason}",
                    "refundReceiveAccount": refund_receive_account}
        r = requests.post(url=f"{BASE_URL}/v1/payments/{payment_key}", json=body)
        return r.json()


toss = DepsTossPayments()

# def test_request():
#     with aiohttp.ClientSession() as session:
#         with session.get(url=f"https://naso-media-backend.herokuapp.com/api/v1/series/update") as r:
#             return r.json()
