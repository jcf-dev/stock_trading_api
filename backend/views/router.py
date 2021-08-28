from fastapi import APIRouter

from .api_v1 import (
    stocks,
    users,
    traders
)

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(stocks.router)
api_router.include_router(traders.router)

