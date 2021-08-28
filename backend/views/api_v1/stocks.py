from fastapi import APIRouter

from ...crud.base_async import CRUDRouterAsync
from ... import models, schemas
from ...deps.db import get_db

router = APIRouter()

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Sector,
        create_schema=schemas.SectorCreate,
        update_schema=schemas.SectorUpdate,
        db_model=models.Sector,
        db=get_db,
        tags=['Sectors'],
        prefix='sectors'
    )
)


router.include_router(
    CRUDRouterAsync(
        schema=schemas.SubSector,
        create_schema=schemas.SubSectorCreate,
        update_schema=schemas.SubSectorUpdate,
        db_model=models.SubSector,
        db=get_db,
        tags=['SubSector'],
        prefix='subsectors'
    )
)

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Stock,
        create_schema=schemas.StockCreate,
        update_schema=schemas.StockUpdate,
        db_model=models.Stock,
        db=get_db,
        tags=['Stocks'],
        prefix='stocks'
    )
)

router.include_router(
    CRUDRouterAsync(
        schema=schemas.PriceHistory,
        create_schema=schemas.PriceHistoryCreate,
        update_schema=schemas.PriceHistoryUpdate,
        db_model=models.PriceHistory,
        db=get_db,
        tags=['PriceHistory'],
        prefix='price-history'
    )
)
