from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .cash_deposit import CashDeposit
    from .cash_usage import CashUsage


class Cash(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cash")
    amount = Column(Integer, default=0, nullable=False)

    deposit = relationship("CashDeposit")
    usage = relationship("CashUsage")
