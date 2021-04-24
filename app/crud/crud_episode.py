from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.series import Series
from app.models.episode import Episode
from app.schemas.episode import EpisodeCreate, EpisodeUpdate

from .utils import get_kst_now, sync_update_date


class CRUDEpisode(CRUDBase[Episode, EpisodeCreate, EpisodeUpdate]):
    def create_with_series(self, db: Session, *, obj_in: EpisodeCreate, series_id: int) -> Episode:
        now = get_kst_now()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, create_at=now, update_at=now,
            series_id=series_id
        )  # type: ignore

        db.add(db_obj)
        sync_update_date(db=db, now=now, series_id=series_id)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Episode,
        obj_in: Union[EpisodeUpdate, Dict[str, Any]]
    ) -> Episode:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, now=db_obj.create_at, episode_id=db_obj.id)
        db.refresh(db_obj)
        return db_obj

    def get_all_with_series_by_order(
        self, db: Session, *, series_id: int
    ) -> List[Episode]:
        return db.query(self.model).filter(self.model.series_id == series_id).order_by(self.model.episode_order).all()

    def get_with_view(
        self, db: Session, *, id: int
    ) -> Episode:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        setattr(db_obj, "view_count", db_obj.view_count + 1)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_latest_by_series(self, db: Session, *, series_id: int) -> Episode:
        return (
            db.query(self.model)
            .filter(self.model.series_id == series_id)
            .order_by(self.model.update_at.asc())
            .first()
        )

    def get_next_order(self, db: Session, *, episode_id: int) -> Episode:
        current = self.get(db, episode_id)
        return (
            db.query(self.model)
            .filter(self.model.series_id == current.series_id)
            .order_by(self.model.episode_order.asc())
            .filter(self.model.episode_order > current.episode_order)
            .first()
        )

    def get_prev_order(self, db: Session, *, episode_id: int) -> Episode:
        current = self.get(db, episode_id)
        return (
            db.query(self.model)
            .filter(self.model.series_id == current.series_id)
            .order_by(self.model.episode_order.desc())
            .filter(self.model.episode_order < current.episode_order)
            .first()
        )


episode = CRUDEpisode(Episode)
