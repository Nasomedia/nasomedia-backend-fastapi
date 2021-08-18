from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .episode import Episode


class Terms(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False)

    episode_id = Column(Integer, ForeignKey(
        "episode.id", ondelete="CASCADE"), nullable=True)
