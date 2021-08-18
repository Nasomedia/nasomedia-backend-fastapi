from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session
import sqlalchemy as sa

from app.crud.base import CRUDBase
from app.models.cash_deposit import CashDeposit
from app.schemas.cash_deposit import CashDepositCreate, CashDepositUpdate
from app.db.session import asyncDB


class CRUDCashDeposit(CRUDBase[CashDeposit, CashDepositCreate, CashDepositUpdate]):
    def get_multi_by_cash_id(
        self, db: Session, cash_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[CashDeposit]:
        return db.query(self.model).filter(self.model.cash_id == cash_id).offset(skip).limit(limit).all()

    def get_by_payment_key(
        self, db: Session, payment_key: str,
    ) -> CashDeposit:
        return db.query(self.model).filter(self.model.payment_key == payment_key).first()

    async def async_update(
        self,
        *,
        db_obj: CashDeposit,
        obj_in: Union[CashDepositUpdate, Dict[str, Any]]
    ) -> Any:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        query = sa\
            .update(CashDeposit)\
            .where(self.model.id == db_obj.id)\
            .values(update_data)
        return await asyncDB.execute(query)

    def remove(self, db: Session, *, id: Any) -> CashDeposit:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


cash_deposit = CRUDCashDeposit(CashDeposit)
