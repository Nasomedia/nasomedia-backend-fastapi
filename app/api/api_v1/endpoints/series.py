from enum import Enum
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/", response_model=List[schemas.Series])
def read_serieses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: str = Query(
        None,
        title="sort criteria",
        description="query string for sort",
        enum=["create_at", "update_at", "id"]
    ),
    order_by: str = Query(
        None,
        title="order by",
        description="query string for order",
        enum=["asc", "desc"]
    ),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve series.
    """
    if crud.user.is_superuser(current_user):
        series = crud.series.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, order_by=order_by)
    # else:
    #     series = crud.series.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return series

@router.post("/", response_model=schemas.Series)
def create_series(
    *,
    db: Session = Depends(deps.get_db),
    series_in: schemas.SeriesCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new series.
    """
    if crud.user.is_superuser(current_user):
        series = crud.series.create(db=db, obj_in=series_in)
    return series


@router.put("/{id}", response_model=schemas.Series)
def update_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    series_in: schemas.SeriesUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an series.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    series = crud.series.update(db=db, db_obj=series, obj_in=series_in)
    return series


@router.get("/{id}", response_model=schemas.Series)
def read_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get series by ID.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series


@router.delete("/{id}", response_model=schemas.Series)
def delete_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an series.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    series = crud.series.remove(db=db, id=id)
    return series


@router.get("/{series_id}/episodes", response_model=List[schemas.Episode])
def read_episodes_with_series_by_order(
    *,
    db: Session = Depends(deps.get_db),
    series_id: int,
) -> Any:
    """
    Retrieve episode with Series by episode order.
    """
    episode = crud.episode.get_all_with_series_by_order(db=db, series_id=series_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.get("/{series_id}/latest", response_model=schemas.Episode)
def read_latest_episode_with_series_by_update(
    *,
    db: Session = Depends(deps.get_db),
    series_id: int,
) -> Any:
    """
    Get latest episode with Series by update date.
    """
    episode = crud.episode.get_latest_by_series(db=db, series_id=series_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode
