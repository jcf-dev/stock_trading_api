from fastapi import APIRouter

from .api import (
    stocks,
    users,
)

api_router = APIRouter()

api_router.include_router(users.router, prefix='/users')
api_router.include_router(stocks.router, prefix='/stocks')
