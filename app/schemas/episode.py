from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

from .episode_image import EpisodeImage


# Shared properties
class EpisodeBase(BaseModel):
    title: Optional[str] = None
    episode_order: Optional[int] = None
    thumbnail: Optional[str] = "/noimage.png"


# Properties to receive on episode creation
class EpisodeCreate(EpisodeBase):
    title: str
    episode_order: int


# Properties to receive on episode update
class EpisodeUpdate(EpisodeBase):
    pass


# Properties shared by models stored in DB
class EpisodeInDBBase(EpisodeBase):
    id: int
    title: str
    series_id: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Episode(EpisodeInDBBase):
    pass


# Properties properties stored in DB
class EpisodeInDB(EpisodeInDBBase):
    pass
