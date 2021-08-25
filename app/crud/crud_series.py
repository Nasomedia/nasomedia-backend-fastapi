from typing import List, Optional, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from app.crud.base import CRUDBase
from app.models.series import Series
from app.schemas.series import SeriesCreate, SeriesUpdate, SeriesSortEnum
from app.schemas import OrderEnum

from .utils import get_kst_now, sync_update_date


class CRUDSeries(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    def get_multi(
        self,
        db: Session,
        *, skip: int = 0, limit: int = 100,
        sort_by: Optional[SeriesSortEnum] = None,
        order_by: Optional[OrderEnum] = "desc",
    ) -> List[Series]:
        if sort_by:
            return db.query(self.model).order_by(text(f"{sort_by} {order_by}")).offset(skip).limit(limit).all()
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: SeriesCreate) -> Series:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.create_at = get_kst_now()
        db.add(db_obj)
        db.commit()
        sync_update_date(db=db, now=db_obj.create_at, series_id=db_obj.id)
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Series,
        obj_in: Union[SeriesUpdate, Dict[str, Any]]
    ) -> Series:
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
        db.refresh(db_obj)
        return db_obj


series = CRUDSeries(Series)
