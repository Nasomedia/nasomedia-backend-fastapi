from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class PurchasePriceBase(BaseModel):
    price: Optional[int]


# Properties to receive on episode creation
class PurchasePriceCreate(PurchasePriceBase):
    price: int


# Properties to receive on episode update
class PurchasePriceUpdate(PurchasePriceBase):
    pass


# Properties shared by models stored in DB
class PurchasePriceInDBBase(PurchasePriceBase):
    id: int
    episode_id: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class PurchasePrice(PurchasePriceInDBBase):
    pass


# Properties properties stored in DB
class PurchasePriceInDB(PurchasePriceInDBBase):
    pass
