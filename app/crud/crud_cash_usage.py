from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cash_usage import CashUsage
from app.schemas.cash_usage import CashUsageCreate, CashUsageUpdate


class CRUDCashUsage(CRUDBase[CashUsage, CashUsageCreate, CashUsageUpdate]):
    def get_multi_by_cash_id(
        self, db: Session, cash_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[CashUsage]:
        return db.query(self.model).filter(self.model.cash_id == cash_id).offset(skip).limit(limit).all()


cash_usage = CRUDCashUsage(CashUsage)
