from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import dtos
import random

from security import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", response_model=dtos.User)
def create_user(form: dtos.UserCreate, db: Session = Depends(models.get_db)):
    user = models.User(**form.model_dump())
    db.add(user)

    db.flush()
    db.refresh(user)

    card = models.Card(
        label="DEFAULT",
        card_no=f"{random.randint(1,9)}" + "".join([str(random.randint(0,9)) for _ in range(15)]),
        user_id=user.id,
        status=models.CardStatus.ACTIVE
    )

    db.add(card)
    db.commit()
    return user



@router.get("/me", response_model=dtos.User)
def get_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user