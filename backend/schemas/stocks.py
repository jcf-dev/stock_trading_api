import datetime

from typing import Optional

from pydantic import BaseModel


class _SectorBase(BaseModel):
    name: str


class _SectorDBBase(_SectorBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class SectorCreate(_SectorBase):
    pass


class SectorUpdate(_SectorBase):
    pass


class Sector(_SectorDBBase):
    pass


class _SubSectorBase(BaseModel):
    name: str


class _SubSectorDBBase(_SubSectorBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class SubSectorCreate(_SubSectorBase):
    pass


class SubSectorUpdate(_SubSectorBase):
    pass


class SubSector(_SubSectorDBBase):
    pass


class _StockBase(BaseModel):
    symbol: str
    name: str
    sector_id: int
    sub_sector_id: int
    listing_date: datetime.date
    active: bool


class _StockDBBase(_StockBase):
    id: Optional[int]

    sector_id: Sector
    sub_sector_id: SubSector

    class Config:
        orm_mode = True


class StockCreate(_StockBase):
    sector_id: Optional[int]
    sub_sector_id: Optional[int]


class StockUpdate(_StockBase):
    pass


class Stock(_StockDBBase):
    pass


class _PriceHistoryBase(BaseModel):
    stock_id: int
    buy: float
    sell: float
    timestamp: datetime.datetime


class _PriceHistoryDBBase(_PriceHistoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class PriceHistoryCreate(_PriceHistoryBase):
    stock_id: Optional[int]


class PriceHistoryUpdate(_PriceHistoryBase):
    pass


class PriceHistory(_PriceHistoryDBBase):
    pass
