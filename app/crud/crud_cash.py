from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cash import Cash
from app.schemas.cash import CashCreate, CashUpdate


class CRUDCash(CRUDBase[Cash, CashCreate, CashUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: CashCreate, user_id: int
    ) -> Cash:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user_id(self, db: Session, user_id: int) -> Cash:
        return db.query(self.model).filter(self.model.user_id == user_id).first()


cash = CRUDCash(Cash)
