from typing import Optional, List

from pydantic import BaseModel
from .cash_deposit import CashDeposit
from .cash_usage import CashUsage


# Shared properties
class CashBase(BaseModel):
    amount: Optional[int] = 0


# Properties to receive on cash creation
class CashCreate(CashBase):
    pass


# Properties to receive on cash update
class CashUpdate(CashBase):
    pass


# Properties shared by models stored in DB
class CashInDBBase(CashBase):
    id: int
    amount: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Cash(CashInDBBase):
    deposit: List[CashDeposit] = []
    usage: List[CashUsage] = []


# Properties properties stored in DB
class CashInDB(CashInDBBase):
    pass
