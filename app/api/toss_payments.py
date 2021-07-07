from app import schemas
import json
from typing import Union, Mapping, TypeVar, Optional
from fastapi.encoders import jsonable_encoder
from multidict import CIMultiDict, CIMultiDictProxy, istr

import aiohttp

from app.core.config import settings

Headers = Union[Mapping[Union[str, istr], str], CIMultiDict, CIMultiDictProxy]

BASE_URL = 'https://api.tosspayments.com'

ClientSessionType = TypeVar("ClientSessionType", bound=aiohttp.ClientSession)


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
        return schemas.PaymentClient(obj_dict)

    async def get_session(self) -> ClientSessionType:
        return await aiohttp.ClientSession(headers=self.headers)

    async def read_payment(self, payment_key: str) -> schemas.Payment:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=f"{BASE_URL}/v1/payments/{payment_key}") as r:
                obj = await r.json()
                return self.serialize_payment(obj)

    async def read_payment_by_order_id(self, order_id: Union[str, int]) -> schemas.Payment:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=f"{BASE_URL}/v1/payments/orders/{order_id}") as r:
                obj = await r.json()
                return self.serialize_payment(obj)

    async def ack_payment(self, payment_key: str, order_id: Union[str, int], amount: int) -> dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url=f"{BASE_URL}/v1/payments/{payment_key}",
                                    json={"orderId": f"{order_id}", "amount": amount}) as r:
                obj = await r.json()
                return self.serialize_payment(obj)

    async def cancel_payment(self, payment_key: str, cancel_reason: str, refund_receive_account: dict = None) -> schemas.Payment:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            if refund_receive_account is None:
                body = {"cancelReason": f"{cancel_reason}", }
            else:
                body = {"cancelReason": f"{cancel_reason}",
                        "refundReceiveAccount": refund_receive_account}
            async with session.post(url=f"{BASE_URL}/v1/payments/{payment_key}", json=body) as r:
                obj = await r.json()
                return self.serialize_payment(obj)


toss = DepsTossPayments()
