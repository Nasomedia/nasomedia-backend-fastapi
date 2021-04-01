from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .episode import Episode


class EpisodeImage(Base):
    __tablename__ = "episode_image"
    id = Column(Integer, primary_key=True, index=True)
    image_order = Column(Integer, index=True)

    # image url
    url = Column(String)

    episode_id = Column(Integer, ForeignKey(
        "episode.id", ondelete="CASCADE"), nullable=False)
    episode = relationship("Episode")
