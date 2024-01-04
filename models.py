from enum import StrEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Double,
    String,
    create_engine,
    text,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import UniqueConstraint

from settings import SETTINGS

Base = declarative_base()


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    PASSIVE = "PASSIVE"
    DELETED = "DELETED"


class BaseModel:
    id = Column(Integer, primary_key=True)
    date_created = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    date_modified = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )


class User(Base, BaseModel):
    __tablename__ = "users"

    password = Column(String(256))
    email = Column(String(100))


class Card(Base, BaseModel):
    __tablename__ = "cards"
    __table_args__ = (UniqueConstraint("card_no", "user_id", name="_card_user_uc"),)

    label = Column(String(100))
    card_no = Column(CHAR(16))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(CardStatus), server_default="PASSIVE")


class Transaction(Base, BaseModel):
    __tablename__ = "transactions"

    amount = Column(Double)
    description = Column(String(256))
    card_id = Column(Integer, ForeignKey("cards.id"))


# Veritabanı bağlantısını oluştur
engine = create_engine(
    f"mysql+mysqlconnector://{SETTINGS.MYSQL_USER}:{SETTINGS.MYSQL_PASSWORD}@mysql-db/{SETTINGS.MYSQL_DATABASE}?charset=utf8mb4"
)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
