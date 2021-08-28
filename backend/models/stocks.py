from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Date, ForeignKey, TIMESTAMP, Integer, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base_class import Base

if TYPE_CHECKING:
    from .traders import Trade, Offer, Portfolio  # noqa: F401

# Stocks based on Philippine Stock Exchange
# https://edge.pse.com.ph/companyDirectory/form.do


class Stock(Base):
    symbol = Column(String(5), index=True, unique=True)
    name = Column(String(256))
    sector_id = Column(Integer, ForeignKey('sector.id'), nullable=True)
    sub_sector_id = Column(Integer, ForeignKey('subsector.id'), nullable=True)
    listing_date = Column(Date(), server_default=func.now())
    active = Column(Boolean(), default=True)

    # FK Reverse Relations
    price_history = relationship("PriceHistory", backref="stock")
    trade = relationship("Trade", backref="stock")
    offer = relationship("Offer", backref="stock")
    portfolio = relationship("Portfolio", backref="stock")

    def __repr__(self):
        return f"<Stock(symbol='{self.symbol}')>"


class PriceHistory(Base):
    stock_id = Column(Integer, ForeignKey('stock.id'))
    buy = Column(Numeric(10, 3))
    sell = Column(Numeric(10, 3))
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<PriceHistory(buy='{self.buy}', sell='{self.sell}')>"


class Sector(Base):
    name = Column(String(50))

    # FK Reverse Relations
    stock = relationship('Stock', backref="sector", uselist=False)

    def __repr__(self):
        return f"<Sector(name='{self.name}')>"


class SubSector(Base):
    name = Column(String(50))

    # FK Reverse Relations
    stock = relationship('Stock', backref="subsector", uselist=False)

    def __repr__(self):
        return f"<SubSector(name='{self.name}')>"
