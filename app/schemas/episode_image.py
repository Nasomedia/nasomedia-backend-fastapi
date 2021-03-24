from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class EpisodeImageBase(BaseModel):
    image_order: Optional[int] = None
    url: Optional[str] = None

# Properties to receive on series creation
class EpisodeImageCreate(EpisodeImageBase):
    image_order: int
    url: str


# Properties to receive on series update
class EpisodeImageUpdate(EpisodeImageBase):
    pass


# Properties shared by models stored in DB
class EpisodeImageInDBBase(EpisodeImageBase):
    id: int
    image_order: int
    url: str
    episode_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class EpisodeImage(EpisodeImageInDBBase):
    pass


# Properties properties stored in DB
class EpisodeImageInDB(EpisodeImageInDBBase):
    pass
