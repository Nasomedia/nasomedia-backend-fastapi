from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.EpisodeImage])
def read_episode_images(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve episode images.
    """
    if crud.user.is_superuser(current_user):
        episode_images = crud.episode_image.get_multi(db, skip=skip, limit=limit)
    # else:
    #     episode_image = crud.episode_image.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return episode_images


@router.post("/", response_model=schemas.EpisodeImage)
def create_episode_image(
    *,
    db: Session = Depends(deps.get_db),
    episode_id: int = Body(...),
    episode_image_in: schemas.EpisodeImageCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new episode image.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud.episode.get(db=db, id=episode_id):
        raise HTTPException(status_code=400, detail="Episode not found. Maybe You've tried to insert wrong number")
    episode_image = crud.episode_image.create_with_episode(
        db=db, obj_in=episode_image_in, episode_id=episode_id)
    return episode_image


@router.put("/{id}", response_model=schemas.EpisodeImage)
def update_episode_image(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    episode_image_in: schemas.EpisodeImageUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an episode image.
    """
    episode_image = crud.episode_image.get(db=db, id=id)
    if not episode_image:
        raise HTTPException(status_code=404, detail="Episode Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    episode_image = crud.episode_image.update(
        db=db, db_obj=episode_image, obj_in=episode_image_in)
    return episode_image


@router.get("/{id}", response_model=schemas.EpisodeImage)
def read_episode_image(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get episode image by ID.
    """
    episode_image = crud.episode_image.get(db=db, id=id)
    if not episode_image:
        raise HTTPException(status_code=404, detail="Episode Image not found")
    return episode_image


@router.delete("/{id}", response_model=schemas.EpisodeImage)
def delete_episode_image(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an episode_image.
    """
    episode_image = crud.episode_image.get(db=db, id=id)
    if not episode_image:
        raise HTTPException(status_code=404, detail="Episode Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    episode_image = crud.episode_image.remove(db=db, id=id)
    return episode_image
