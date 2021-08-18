from app.utils import get_kst_now
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.api import deps

router = APIRouter()


@router.post("/order", response_model=schemas.CashDeposit)
def create_cash_deposit(
    *,
    db: Session = Depends(deps.get_db),
    cash_deposit_in: schemas.CashDepositRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new cash deposit.
    """
    cash_deposit_in = schemas.CashDepositCreate(**cash_deposit_in.dict())

    cash = crud.cash.get_by_user_id(db, current_user.id)

    if cash_deposit_in.cash_id != cash.id:
        raise HTTPException(status_code=400, detail="Invalid Cash Information")

    if cash_deposit_in.deposit_amount < 1000 or cash_deposit_in.deposit_amount % 1000 != 0:
        raise HTTPException(status_code=400, detail="Invalid Amount Value")

    cash_deposit = crud.cash_deposit.create(db=db, obj_in=cash_deposit_in)
    return cash_deposit


@router.delete("/order/{id}", response_model=schemas.CashDeposit)
def delete_cash_deposit(
    *,
    db: Session = Depends(deps.get_db),
    id: Union[str, Any],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete cash deposit.
    """
    cash = crud.cash.get_by_user_id(db, current_user.id)
    cash_deposit_in = crud.cash_deposit.get(db, id)
    if cash_deposit_in.cash_id != cash.id:
        raise HTTPException(status_code=400, detail="Invalid Cash Information")
    cash_deposit = crud.cash_deposit.remove(db=db, obj_in=cash_deposit_in)
    return cash_deposit


@router.post("/ack", response_model=List[Union[schemas.Cash, schemas.CashDeposit, schemas.PaymentClient]])
async def acknowledgment_cash_deposit(
    *,
    db: Session = Depends(deps.get_db),
    payment_key: str,
    order_id: Union[Any, str],
    amount: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    acknowledgment cash deposit.
    """
    cash_deposit_obj = crud.cash_deposit.get(db, id=order_id)
    if not cash_deposit_obj:
        raise HTTPException(status_code=400, detail="Invalid order id")

    if cash_deposit_obj.payment_key:
        raise HTTPException(status_code=400, detail="Already processed payment")

    cash = crud.cash.get_by_user_id(db, current_user.id)
    if cash_deposit_obj.cash_id != cash.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if amount != cash_deposit_obj.deposit_amount:
        raise HTTPException(status_code=400, detail="Invalid Amount Value")
    ack_info = await deps.toss.ack_payment(payment_key=payment_key, order_id=order_id, amount=amount)
    ack_info: schemas.Payment = deps.toss.serialize_payment(ack_info)
    if ack_info.status != "DONE":
        raise HTTPException(status_code=400, detail="Failed to payment")
    if ack_info.approvedAt:
        cash_deposit_in = schemas.CashDepositUpdate(
            payment_key=ack_info.paymentKey,
            ack_at=ack_info.approvedAt,
            approved_at=ack_info.approvedAt,
        )
        cash = crud.cash.update(db, db_obj=cash, obj_in=schemas.CashUpdate(
            amount=cash.amount+cash_deposit_obj.deposit_amount))
    else:
        cash_deposit_in = schemas.CashDepositUpdate(
            payment_key=ack_info.paymentKey,
            ack_at=get_kst_now(),
            due_date=ack_info.virtualAccount.dueDate,
            secret=ack_info.secret
        )

    await crud.cash_deposit.async_update(
        db_obj=cash_deposit_obj, obj_in=cash_deposit_in)
    cash_deposit = crud.cash_deposit.get(db, id=order_id)
    return [cash, cash_deposit, deps.toss.encapsulate_payment_for_client(ack_info)]


@router.post("/callback")
def cash_deposit_callback(
    *,
    db: Session = Depends(deps.get_db),
    callback_in: schemas.PaymentCallbackRequest
) -> Any:
    """
    cash deposit approve callback
    """
    cash_deposit = crud.cash_deposit.get(db, id=callback_in.orderId)
    if not cash_deposit:
        raise HTTPException(
            status_code=400, detail=f"OrderId: {callback_in.orderId} not found")
    if cash_deposit.secret != callback_in.secret:
        raise HTTPException(
            status_code=400, detail="Invalid request, You shoud check secret key")

    if callback_in.status == "DONE":
        crud.cash_deposit.update(db, db_obj=cash_deposit, obj_in=schemas.CashDepositUpdate(
            approved_at=get_kst_now()
        ))

        cash = crud.cash.get(db, cash_deposit.cash_id)
        crud.cash.update(db=db, db_obj=cash, obj_in=schemas.CashUpdate(
            amount=cash.amount+cash_deposit.deposit_amount))

    elif callback_in.status == "CANCEL":
        crud.cash_deposit.update(db, db_obj=cash_deposit, obj_in=schemas.CashDepositUpdate(
            is_cancel=True
        ))

    return {"status": "DONE", "detail": "Successfuly Update Cash"}


@router.post("/cancel", response_model=List[Union[schemas.Cash, schemas.CashDeposit]])
async def cancel_cash_deposit(
    *,
    db: Session = Depends(deps.get_db),
    payment_key: str,
    cancel_reason: str = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    cancel cash deposit.
    """
    cash_deposit_obj = crud.cash_deposit.get_by_payment_key(db, payment_key=payment_key)
    if not cash_deposit_obj:
        raise HTTPException(status_code=400, detail="Invalid payment key")

    cash = crud.cash.get_by_user_id(db, current_user.id)
    if cash_deposit_obj.cash_id != cash.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    cancel_info = await deps.toss.cancel_payment(payment_key=payment_key, cancel_reason=cancel_reason, refund_receive_account=None)
    cancel_info = deps.toss.serialize_payment(cancel_info)
    if cancel_info.status != "PARTIAL_CANCELED":
        raise HTTPException(status_code=400, detail="Failed to cancel payment")

    if cancel_info.approvedAt is not None:
        crud.cash.update(db, db_obj=cash, obj_in=schemas.CashUpdate(
            amount=cash.amount-cash_deposit_obj.deposit_amount))

    cash_deposit = crud.cash_deposit.update(
        db=db, db_obj=cash_deposit_obj, obj_in=schemas.CashDepositUpdate(is_cancel=True))
    return [cash, cash_deposit]
