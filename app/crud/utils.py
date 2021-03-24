from pytz import timezone
from datetime import datetime

from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.series import Series
from app.models.episode import Episode

from sqlalchemy.orm import exc as sa_exc


def get_kst_now() -> datetime:
    return datetime.now(timezone("Asia/Seoul"))


def refresh_all(db: Session, instances: List) -> List:
    """Refresh the given collection of instances to this ``Session``."""
    refreshed_instance = list()
    for instance in instances:
        db.refresh(instance)
        refreshed_instance.append(instance)
    return refreshed_instance


def sync_update_date(
    db: Session,
    now: datetime = get_kst_now(),
    episode_id: int = None,
    series_id: int = None
) -> None:
    if episode_id:
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        episode.update_at = now
        
        if series_id:
            series = db.query(Series).filter(Series.id == series_id).first()
            series.update_at = now
        if not series_id:
            series = db.query(Series).filter(Series.id == episode.series_id).first()
            series.update_at = now
            
        db.add_all([series, episode])

    elif not episode_id and series_id:
        series = db.query(Series).filter(Series.id == series_id).first()
        series.update_at = now
        db.add(series)

    else:
        raise sa_exc.InvalidRequestError(
            "No target specified for sync date."
        )
    db.commit()
