from fastapi import FastAPI

from routes.card import router as card_router
from routes.transaction import router as transaction_router
from routes.user import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(card_router)
app.include_router(transaction_router)
