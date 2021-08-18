from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from app.models._guid import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy.orm import relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from .cash import Cash


class CashDeposit(Base):
    __tablename__ = "cash_deposit"
    id = Column(
        GUID,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    description = Column(String, nullable=True)

    deposit_amount = Column(Integer, nullable=False)

    request_at = Column(DateTime(timezone=True), index=True)
    ack_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

    is_cancel = Column(Boolean(), default=False)

    cash_id = Column(Integer, ForeignKey(
        "cash.id", ondelete="CASCADE"), nullable=False
    )

    payment_key = Column(String, nullable=True)
    due_date = Column(DateTime(timezone=True))
    secret = Column(String, nullable=True)