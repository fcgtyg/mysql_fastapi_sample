import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import dtos
import models
from security import get_current_user

router = APIRouter(prefix="/card", tags=["Card"])


@router.post("", response_model=dtos.Card)
def create_card(
    form: dtos.CardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    card = models.Card(**form.model_dump(), user_id=current_user.id)

    db.add(card)
    db.commit()
    return card


@router.get("/me", response_model=list[dtos.Card])
def get_cards(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    cards = db.scalars(
        select(models.Card)
        .where(
            models.Card.user_id == current_user.id,
            models.Card.status != models.CardStatus.DELETED,
        )
        .order_by(models.Card.date_created)
    ).all()
    return cards


@router.put("/{card_id}", response_model=dtos.Card)
def update_card(
    card_id: int,
    form: dtos.CardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    card = db.scalar(
        select(models.Card).where(
            models.Card.user_id == current_user.id,
            models.Card.status != models.CardStatus.DELETED,
            models.Card.id == card_id,
        )
    )

    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    card.date_modified = datetime.datetime.now()
    card.label = form.label
    card.card_no = form.card_no
    card.status = form.status

    db.commit()

    return card


@router.delete("/{card_id}", response_model=dtos.Card)
def delete_card(
    card_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(models.get_db),
):
    active_card_status = db.scalar(
        select(func.count()).where(
            models.Card.user_id == current_user.id,
            models.Card.status == models.CardStatus.ACTIVE,
        )
    )
    if active_card_status <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one card must remain active!",
        )
    card = db.scalar(
        select(models.Card).where(
            models.Card.user_id == current_user.id,
            models.Card.status != models.CardStatus.DELETED,
            models.Card.id == card_id,
        )
    )

    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    card.status = models.CardStatus.DELETED

    db.commit()

    return card
