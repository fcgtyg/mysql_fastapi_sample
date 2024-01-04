from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import dtos
import models
from security import get_current_user

router = APIRouter(prefix="/tranaction", tags=["Transaction"])


@router.post("", response_model=dtos.Transaction)
def create_transaction(
    form: dtos.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    card = db.scalar(
        select(models.Card).where(
            models.Card.id == form.card_id,
            models.Card.user_id == current_user.id,
            models.Card.status == models.CardStatus.ACTIVE,
        )
    )

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found"
        )

    transaction = models.Transaction(**form.model_dump())

    db.add(transaction)
    db.commit()
    return transaction


@router.get("/me", response_model=list[dtos.Transaction])
def get_transactions(
    card_label_search: str | None = None,
    card_id: str | None = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    filters = [
        models.Card.user_id == current_user.id,
        models.Card.status != models.CardStatus.DELETED,
    ]
    if card_label_search:
        filters.append(models.Card.label.ilike(f"%{card_label_search}%"))

    if card_id:
        filters.append(models.Card.id == card_id)

    transactions = db.scalars(
        select(models.Transaction)
        .join(models.Card, models.Card.id == models.Transaction.card_id)
        .where(*filters)
        .order_by(models.Transaction.date_created)
    ).all()
    return transactions


@router.get("/summary", response_model=dtos.TransactionSummary)
def get_transaction_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    active_card_count = (
        db.query(func.count())
        .select_from(models.Card)
        .filter(models.Card.status == "ACTIVE", models.Card.user_id == current_user.id)
        .scalar()
    )

    # Toplam harcama yapılan tutar
    total_spent_amount = (
        db.query(func.sum(models.Transaction.amount))
        .join(models.Card)
        .filter(models.Card.status == "ACTIVE", models.Card.user_id == current_user.id)
        .scalar()
    ) or 0

    # Pasif kartlarda toplam harcama yapılan tutar
    total_spent_amount_passive = (
        db.query(func.sum(models.Transaction.amount))
        .join(models.Card)
        .filter(models.Card.status == "PASSIVE", models.Card.user_id == current_user.id)
        .scalar()
    ) or 0

    return dtos.TransactionSummary(
        active_card_count=active_card_count,
        total_spent_amount=total_spent_amount,
        total_spent_amount_passive=total_spent_amount_passive,
    )
