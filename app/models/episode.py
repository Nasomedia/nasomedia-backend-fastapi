from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relation, relationship

from app.db.base_class import Base
from app.models.purchase_price import PurchasePrice

if TYPE_CHECKING:
    from .series import Series
    from .episode_image import EpisodeImage


class Episode(Base):
    __tablename__ = "episode"
    id = Column(Integer, primary_key=True, index=True)
    episode_order = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)

    create_at = Column(DateTime(timezone=True))
    update_at = Column(DateTime(timezone=True))

    series_id = Column(Integer, ForeignKey(
        "series.id", ondelete="CASCADE"), nullable=False)
    series = relationship("Series")

    # thumbnail image url
    thumbnail = Column(String)

    view_count = Column(Integer, default=0, nullable=False)

    purchase_price = relationship(PurchasePrice, uselist=False, backref="episode")
