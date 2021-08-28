import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel

from .stocks import Stock
from .users import User


class _OfferBase(BaseModel):
    trader_id: int
    stock_id: int
    quantity: float
    buy: bool
    sell: bool
    price: float
    timestamp: datetime.datetime


class OfferCreate(_OfferBase):
    pass


class OfferUpdate(_OfferBase):
    pass


class _TraderBase(BaseModel):
    fname: str
    lname: str
    user_id: int
    active: bool
    updated: datetime.datetime
    created: datetime.datetime


class _TraderDBBase(_TraderBase):
    id: Optional[int]

    user_id: Optional[User]

    class Config:
        orm_mode = True


class TraderCreate(_TraderBase):
    user_id: Optional[int]


class TraderUpdate(_TraderBase):
    pass


class Trader(_TraderDBBase):
    pass


class _TradeBase(BaseModel):
    stock_id: int
    seller_id: int
    buyer_id: int
    quantity: float
    unit_price: float
    offer_id: Optional[uuid.UUID]


class _OfferDBBase(_OfferBase):
    id: uuid.UUID = uuid.uuid4()

    trader_id: Optional[Trader]
    stock_id: Optional[Trader]

    class Config:
        orm_mode = True


class Offer(_OfferDBBase):
    pass


class _TradeDBBase(_TradeBase):
    id: Optional[int]

    stock_id: Optional[Stock]
    seller_id: Optional[Trader]
    buyer_id: Optional[Trader]

    offer_id: Optional[List[Offer]]

    class Config:
        orm_mode = True


class TradeCreate(_TradeBase):
    pass


class TradeUpdate(_TradeBase):
    pass


class Trade(_TradeDBBase):
    pass


class _PortfolioBase(BaseModel):
    trader_id: int
    stock_id: int
    quantity: float


class _PortfolioDBBase(_PortfolioBase):
    id: Optional[int]

    trader_id: Optional[Trader]
    stock_id: Optional[Stock]

    class Config:
        orm_mode = True


class PortfolioCreate(_PortfolioBase):
    pass


class PortfolioUpdate(_PortfolioBase):
    pass


class Portfolio(_PortfolioDBBase):
    pass
