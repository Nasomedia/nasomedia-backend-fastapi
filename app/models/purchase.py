from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .terms import Terms


class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    terms_id = Column(Integer, ForeignKey(
        "terms.id", ondelete="CASCADE"), nullable=False)
