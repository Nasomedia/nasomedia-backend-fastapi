from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.series import SeriesCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_series(db: Session, *, owner_id: Optional[int] = None) -> models.Series:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    series_in = SeriesCreate(title=title, description=description, id=id)
    return crud.series.create_with_owner(db=db, obj_in=series_in, owner_id=owner_id)
