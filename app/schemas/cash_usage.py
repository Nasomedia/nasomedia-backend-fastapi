from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class CashUsageBase(BaseModel):
    deposit_amount: Optional[int] = 0
    description: Optional[str]


# Properties to receive on cash usage creation
class CashUsageCreate(CashUsageBase):
    usage_amount: int
    cash_id: int
    description: str


# Properties to receive on cash usage update
class CashUsageUpdate(CashUsageBase):
    pass


# Properties shared by models stored in DB
class CashUsageInDBBase(CashUsageBase):
    id: int
    description: str
    deposit_amount: int
    cash_id: int
    usage_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class CashUsage(CashUsageInDBBase):
    pass


# Properties properties stored in DB
class CashUsageInDB(CashUsageInDBBase):
    pass
