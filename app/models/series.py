from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True)

    update_at = Column(DateTime(timezone=True))
    create_at = Column(DateTime(timezone=True))

    thumbnail = Column(String)

    is_complete = Column(Boolean(), default=False)
