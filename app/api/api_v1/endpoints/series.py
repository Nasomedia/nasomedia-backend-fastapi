from enum import Enum
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Series])
def read_series(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = Query(
        "id",
        title="sort criteria",
        description="query string for sort",
        enum=["create_at", "update_at", "id", "title"]
    ),
    order_by: Optional[str] = Query(
        "asc",
        title="order by",
        description="query string for order",
        enum=["asc", "desc"]
    ),

    title: Optional[str] = Query(
        None,
        title="filter title",
        description="filter for title"
    ),
    is_complete: Optional[bool] = Query(
        None,
        title="filter is_complete",
        description="filter for is series complete"
    ),
    keyword: Optional[str] = Query(
        None,
        title="search keyword"
    )
) -> Any:
    """
    Retrieve series.
    """
    kwargs = {}
    if title:
        kwargs["title"] = title
    if is_complete:
        kwargs["is_complete"] = is_complete
    series = crud.series.get_multi(
        db, skip=skip, limit=limit, sort_by=sort_by,
        order_by=order_by, keyword=keyword, **kwargs
    )
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

@router.get("/{id}/episodes", response_model=List[schemas.Episode])
def read_series_episodes(
    *,
    db: Session = Depends(deps.get_db),
    series_id: int,
) -> Any:
    """
    Retrieve episode with Series by episode order.
    """
    episode = crud.episode.get_all_with_series(db=db, series_id=series_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode