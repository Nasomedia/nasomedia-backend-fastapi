from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .cash import Cash


class CashUsage(Base):
    __tablename__ = "cash_usage"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

    usage_at = Column(DateTime(timezone=True), index=True)
    usage_amount = Column(Integer, nullable=False)

    cash_id = Column(Integer, ForeignKey(
        "cash.id", ondelete="CASCADE"), nullable=False)
