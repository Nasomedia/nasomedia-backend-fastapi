from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Series])
def read_series(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve series.
    """
    if crud.user.is_superuser(current_user):
        series = crud.series.get_multi(db, skip=skip, limit=limit)
    else:
        series = crud.series.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return series


@router.post("/", response_model=schemas.Series)
def create_series(
    *,
    db: Session = Depends(deps.get_db),
    series_in: schemas.SeriesCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new series.
    """
    series = crud.series.create_with_owner(db=db, obj_in=series_in, owner_id=current_user.id)
    return series


@router.put("/{id}", response_model=schemas.Series)
def update_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    series_in: schemas.SeriesUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an series.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    if not crud.user.is_superuser(current_user) and (series.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    series = crud.series.update(db=db, db_obj=series, obj_in=series_in)
    return series


@router.get("/{id}", response_model=schemas.Series)
def read_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get series by ID.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    if not crud.user.is_superuser(current_user) and (series.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return series


@router.delete("/{id}", response_model=schemas.Series)
def delete_series(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an series.
    """
    series = crud.series.get(db=db, id=id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    if not crud.user.is_superuser(current_user) and (series.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    series = crud.series.remove(db=db, id=id)
    return series
