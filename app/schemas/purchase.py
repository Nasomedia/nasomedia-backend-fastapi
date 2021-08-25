from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class PurchaseBase(BaseModel):
    pass


# Properties to receive on episode creation
class PurchaseCreate(PurchaseBase):
    pass


# Properties to receive on episode update
class PurchaseUpdate(PurchaseBase):
    pass


# Properties shared by models stored in DB
class PurchaseInDBBase(PurchaseBase):
    id: int
    user_id: int
    price_id: int
    create_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Purchase(PurchaseInDBBase):
    pass


# Properties properties stored in DB
class PurchaseInDB(PurchaseInDBBase):
    pass
