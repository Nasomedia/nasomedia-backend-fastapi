from app.models import cash_deposit
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=Union[List[schemas.Cash], schemas.Cash])
def read_cash(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cash.
    """
    if crud.user.is_superuser(current_user):
        cash = crud.cash.get_multi(db, skip=skip, limit=limit)
    else:
        cash = crud.cash.get_by_user_id(db=db, user_id=current_user.id)
        if not cash:
            cash = crud.cash.create_with_user(
                db=db, obj_in=schemas.cash.CashCreate(), user_id=current_user.id
            )
    return cash


@router.post("/", response_model=schemas.Cash)
def create_cash(
    *,
    db: Session = Depends(deps.get_db),
    cash_in: schemas.CashCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new cash.
    """
    if crud.cash.get_by_user_id(db, current_user.id):
        raise HTTPException(status_code=400, detail="You have cash info aleady.")
    cash = crud.cash.create_with_user(
        db=db, obj_in=cash_in, user_id=current_user.id
    )
    return cash


@router.put("/", response_model=schemas.Cash)
def update_cash(
    *,
    db: Session = Depends(deps.get_db),
    cash_in: schemas.CashUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an cash my account.
    """
    cash = crud.cash.get_by_user_id(db=db, user_id=current_user.id)
    if not cash:
        raise HTTPException(status_code=404, detail="Cash not found")
    cash = crud.cash.update(db=db, db_obj=cash, obj_in=cash_in)
    return cash


@router.delete("/", response_model=schemas.Cash)
def delete_cash(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an cash.
    """
    cash = crud.cash.get_by_user_id(db=db, user_id=current_user.id)
    if not cash:
        raise HTTPException(status_code=404, detail="Cash not found")
    cash = crud.cash.remove(db=db, id=id)
    return cash


@router.get("/deposit", response_model=Union[List[schemas.CashDeposit], schemas.CashDeposit])
def read_cash_deposit(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cash deposit.
    """
    if crud.user.is_superuser(current_user):
        cash_deposits = crud.cash_deposit.get_multi(db, skip=skip, limit=limit)
    else:
        cash = crud.cash.get_by_user_id(db, current_user.id)
        if not cash:
            cash = crud.cash.create_with_user(
                db=db, obj_in=schemas.cash.CashCreate(), user_id=current_user.id
            )
        cash_deposits = crud.cash_deposit.get_multi_by_cash_id(
            db=db, cash_id=cash.id, skip=skip, limit=limit
        )
    return cash_deposits


@router.get("/usage", response_model=Union[List[schemas.CashUsage], schemas.CashUsage])
def read_cash_usage(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cash usage.
    """
    if crud.user.is_superuser(current_user):
        cash_usages = crud.cash_usage.get_multi(db, skip=skip, limit=limit)
    else:
        cash = crud.cash.get_by_user_id(db, current_user.id)
        if not cash:
            cash = crud.cash.create_with_user(
                db=db, obj_in=schemas.cash.CashCreate(), user_id=current_user.id
            )
        cash_usages = crud.cash_usage.get_multi_by_cash_id(
            db=db, cash_id=cash.id, skip=skip, limit=limit
        )
    return cash_usages
