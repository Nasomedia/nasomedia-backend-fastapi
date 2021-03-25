from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.episode import Episode
from app.models.episode_image import EpisodeImage
from app.schemas.episode_image import EpisodeImageCreate, EpisodeImageUpdate

from .utils import get_kst_now, refresh_all, sync_update_date


class CRUDEpisodeImage(CRUDBase[EpisodeImage, EpisodeImageCreate, EpisodeImageUpdate]):
    def create_with_episode(self, db: Session, *, obj_in: EpisodeImageCreate, episode_id: int) -> EpisodeImage:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, episode_id=episode_id)  # type: ignore

        sync_update_date(db=db, episode_id=episode_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi_with_episode(
        self, db: Session, *, obj_in_list: List[EpisodeImageCreate], episode_id: int
    ) -> List[EpisodeImage]:
        db_obj_list = list()
        for obj_in in obj_in_list:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data, episode_id=episode_id)  # type: ignore
            db_obj_list.append(db_obj)

        sync_update_date(db=db, episode_id=episode_id)

        db.add_all(db_obj_list)
        db.commit()
        db_obj_list = refresh_all(db, db_obj_list)
        return db_obj_list

    def update(
        self,
        db: Session,
        *,
        db_obj: EpisodeImage,
        obj_in: Union[EpisodeImageUpdate, Dict[str, Any]]
    ) -> EpisodeImage:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_at = get_kst_now()


        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, episode_id=db_obj.episode_id)
        db.refresh(db_obj)
        return db_obj

    def update_multi(
        self,
        db: Session,
        *,
        db_obj_list: List[EpisodeImage],
        obj_in_list: List[Union[EpisodeImageUpdate, Dict[str, Any]]]
    ) -> List[EpisodeImage]:
        now = get_kst_now()
        update_db_obj_list = list()
        for db_obj, obj_in in db_obj_list, obj_in_list:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db_obj.update_at = now
            update_db_obj_list.append(db_obj)


        db.add_all(update_db_obj_list)
        db.commit()
        sync_update_date(db=db, episode_id=db_obj.episode_id)
        update_db_obj_list = refresh_all(db, update_db_obj_list)
        return update_db_obj_list

    def get_all_with_episode_by_order(
        self, db: Session, *, episode_id: int
    ) -> List[EpisodeImage]:
        return db.query(self.model).filter(self.model.episode_id == episode_id).order_by(self.model.image_order).all()


episode_image = CRUDEpisodeImage(EpisodeImage)
