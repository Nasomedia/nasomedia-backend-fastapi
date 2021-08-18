from typing import Any, Optional, List
from datetime import datetime

from pydantic import BaseModel
from fastapi import UploadFile, File, Form
import ast


# Shared properties
class EpisodeImageBase(BaseModel):
    image_order: Optional[int] = None
    url: Optional[str] = None


# Properties to receive on http request
class EpisodeImageFileRequest(BaseModel):
    episode_id: int
    order_in_list: List[int]
    episode_image_in_list: List[UploadFile]

    @classmethod
    def as_form(
        cls,
        episode_id: int = Form(...),
        order_in_str: str = Form(...),
        episode_image_in_list: List[UploadFile] = File(...)
    ) -> Any:
        return cls(episode_id=episode_id, order_in_list=ast.literal_eval(order_in_str), episode_image_in_list=episode_image_in_list)


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
