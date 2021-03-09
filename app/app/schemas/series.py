from typing import Optional

from pydantic import BaseModel


# Shared properties
class SeriesBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on series creation
class SeriesCreate(SeriesBase):
    title: str


# Properties to receive on series update
class SeriesUpdate(SeriesBase):
    pass


# Properties shared by models stored in DB
class SeriesInDBBase(SeriesBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Series(SeriesInDBBase):
    pass


# Properties properties stored in DB
class SeriesInDB(SeriesInDBBase):
    pass
