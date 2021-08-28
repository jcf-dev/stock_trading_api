from fastapi import APIRouter

from ...crud.base_async import CRUDRouterAsync
from ... import models, schemas
from ...deps.db import get_db

router = APIRouter()

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Trader,
        create_schema=schemas.TraderCreate,
        update_schema=schemas.TraderUpdate,
        db_model=models.Trader,
        db=get_db,
        tags=['Trader'],
        prefix='trader'
    )
)

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Trade,
        create_schema=schemas.TradeCreate,
        update_schema=schemas.TradeUpdate,
        db_model=models.Trade,
        db=get_db,
        tags=['Trade'],
        prefix='trade'
    )
)

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Offer,
        create_schema=schemas.OfferCreate,
        update_schema=schemas.OfferUpdate,
        db_model=models.Offer,
        db=get_db,
        tags=['Offer'],
        prefix='offer'
    )
)

router.include_router(
    CRUDRouterAsync(
        schema=schemas.Portfolio,
        create_schema=schemas.PortfolioCreate,
        update_schema=schemas.PortfolioUpdate,
        db_model=models.Portfolio,
        db=get_db,
        tags=['Portfolio'],
        prefix='portfolio'
    )
)


