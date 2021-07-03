from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class CashDepositBase(BaseModel):
    deposit_amount: Optional[int] = 0
    description: Optional[str]
    payment_key: Optional[str]
    request_at: Optional[datetime]
    ack_at: Optional[datetime]
    approved_at: Optional[datetime]
    is_cancel: Optional[bool] = False


# Properties to receive on cash deposit creation
class CashDepositCreate(CashDepositBase):
    deposit_amount: int
    cash_id: int
    request_at: datetime
    description: Optional[str]


# Properties to receive on cash deposit creation
class CashDepositRequest(BaseModel):
    deposit_amount: int
    cash_id: int
    request_at: datetime


# Properties to receive on cash deposit update
class CashDepositUpdate(CashDepositBase):
    pass


# Properties shared by models stored in DB
class CashDepositInDBBase(CashDepositBase):
    id: int
    deposit_amount: int
    cash_id: int
    request_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class CashDeposit(CashDepositInDBBase):
    pass


# Properties properties stored in DB
class CashDepositInDB(CashDepositInDBBase):
    pass
