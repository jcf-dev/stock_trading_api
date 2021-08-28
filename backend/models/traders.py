import uuid

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Integer, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base_class import Base

if TYPE_CHECKING:
    from .stocks import Stock  # noqa: F401


class Trader(Base):
    fname = Column(String(64))
    lname = Column(String(64))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    active = Column(Boolean, default=False)  # Need email confirmation to be True
    updated = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # FK Reverse Relations (`uselist` tells the SQLAlchemy that this is a one-to-one relationship)
    offer = relationship("Offer", backref="trader")
    portfolio = relationship("Portfolio", backref="trader")

    seller = relationship("Trade", backref="seller", primaryjoin="Trader.id==Trade.seller_id")
    buyer = relationship("Trade", backref="buyer", primaryjoin="Trader.id==Trade.buyer_id")

    def __repr__(self):
        return f"<Trader(fname='{self.fname}', lname='{self.lname}')>"


class Trade(Base):
    stock_id = Column(Integer, ForeignKey('stock.id'))
    seller_id = Column(Integer, ForeignKey('trader.id'))
    buyer_id = Column(Integer, ForeignKey('trader.id'))
    quantity = Column(Numeric(10, 3))
    unit_price = Column(Numeric(10, 3))
    offer_id = Column(UUID(as_uuid=True), ForeignKey('offer.id'))

    def __repr__(self):
        return f"<Trade(stock_id='{self.stock_id}', quantity='{self.quantity}, unit_price='{self.unit_price}')>"


class Offer(Base):
    id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4(), primary_key=True)
    trader_id = Column(Integer, ForeignKey('trader.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    quantity = Column(Numeric(10, 3))
    buy = Column(Boolean(), default=False)
    sell = Column(Boolean(), default=False)
    price = Column(Numeric(10, 3))
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    # FK Reverse Relations
    trade = relationship("Trade", backref="offer")

    def __repr__(self):
        return f"<Offer(trader_id='{self.trade_id}', stock_id='{self.stock_id}', " \
               f"quantity='{self.quantity}, unit_price='{self.unit_price}')>"


class Portfolio(Base):
    trader_id = Column(Integer, ForeignKey('trader.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    quantity = Column(Numeric(10, 3))

    def __repr__(self):
        return f"<Portfolio(trader_id='{self.trade_id}', stock_id='{self.stock_id}')>"
