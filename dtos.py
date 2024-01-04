import random
from datetime import datetime
from typing import Literal

import bcrypt
from pydantic import BaseModel, model_validator

import models


class BaseDTO(BaseModel):
    id: int
    date_created: datetime = datetime.now()
    date_modified: datetime = datetime.now()


class User(BaseDTO):
    email: str


class UserCreate(BaseModel):
    email: str
    password: str

    @model_validator(mode="after")
    def hash_password(self):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(self.password.encode("utf-8"), salt)
        return self


class CardCreate(BaseModel):
    label: str
    card_no: str | None = None
    status: Literal["ACTIVE"] | Literal["PASSIVE"] = "ACTIVE"

    @model_validator(mode="after")
    def generate_card_number(self):
        if self.card_no:
            return self

        self.card_no = f"{random.randint(1,9)}" + "".join(
            [str(random.randint(0, 9)) for _ in range(15)]
        )
        return self


class Card(BaseDTO, CardCreate):
    status: models.CardStatus


class TransactionCreate(BaseModel):
    amount: float
    description: str
    card_id: int


class Transaction(BaseDTO, TransactionCreate):
    ...


class TransactionSummary(BaseModel):
    active_card_count: int
    total_spent_amount: float = 0
    total_spent_amount_passive: float = 0
