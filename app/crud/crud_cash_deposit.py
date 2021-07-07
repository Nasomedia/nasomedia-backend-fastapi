from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cash_deposit import CashDeposit
from app.schemas.cash_deposit import CashDepositCreate, CashDepositUpdate


class CRUDCashDeposit(CRUDBase[CashDeposit, CashDepositCreate, CashDepositUpdate]):
    def get_multi_by_cash_id(
        self, db: Session, cash_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[CashDeposit]:
        return db.query(self.model).filter(self.model.cash_id == cash_id).offset(skip).limit(limit).all()

    def get_by_payment_key(
        self, db: Session, payment_key: int,
    ) -> CashDeposit:
        return db.query(self.model).filter(self.model.payment_key == payment_key).first()

    def remove_all(self, db: Session):
        db.query(self.model).delete()


cash_deposit = CRUDCashDeposit(CashDeposit)
