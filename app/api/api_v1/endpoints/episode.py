from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Episode])
def read_episodes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve episode.
    """
    if crud.user.is_superuser(current_user):
        episode = crud.episode.get_multi(db, skip=skip, limit=limit)
    # else:
    #     episode = crud.episode.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return episode


@router.post("/", response_model=schemas.Episode)
def create_episode(
    *,
    db: Session = Depends(deps.get_db),
    episode_in: schemas.EpisodeCreate,
    series_id: int = Body(...),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new episode.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud.series.get(db=db, id=series_id):
        raise HTTPException(
            status_code=400, detail="Episode not found. Maybe You've tried to insert wrong number")
    episode = crud.episode.create_with_series(
        db=db, obj_in=episode_in, series_id=series_id)
    return episode


@router.put("/{id}", response_model=schemas.Episode)
def update_episode(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    episode_in: schemas.EpisodeUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an episode.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    episode = crud.episode.update(db=db, db_obj=episode, obj_in=episode_in)
    return episode


@router.get("/{id}", response_model=schemas.Episode)
def read_episode(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get episode by ID.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.get("/{id}", response_model=schemas.Episode)
def get_prev_episode(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get prev episode by ID.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Current Episode not found")
    prev_episode = crud.episode.get_prev_order(db=db, episode_id=id)
    if not prev_episode:
        raise HTTPException(status_code=404, detail="Previous Episode is not exist")
    return prev_episode


@router.get("/{id}", response_model=schemas.Episode)
def get_next_episode(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get next episode by ID.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Current Episode not found")
    next_episode = crud.episode.get_next_order(db=db, episode_id=id)
    if not next_episode:
        raise HTTPException(status_code=404, detail="Next Episode is not exist")
    return next_episode


@router.delete("/{id}", response_model=schemas.Episode)
def delete_episode(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an episode.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    episode = crud.episode.remove(db=db, id=id)
    return episode


@router.get("/{episode_id}/images", response_model=List[schemas.EpisodeImage])
def read_episode_images_with_episode_by_order(
    *,
    db: Session = Depends(deps.get_db),
    episode_id: int,
) -> Any:
    """
    Retrieve episode images with Episode by order.
    """
    episode_images = crud.episode_image.get_all_with_episode_by_order(
        db=db, episode_id=episode_id)
    if not episode_images:
        raise HTTPException(status_code=404, detail="Episode Image not found")
    return episode_images
