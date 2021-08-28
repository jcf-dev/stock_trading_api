from fastapi import APIRouter

from ...crud.base_async import CRUDRouterAsync
from ... import models, schemas
from ...deps.db import get_db

router = APIRouter()

router.include_router(
    CRUDRouterAsync(
        schema=schemas.User,
        create_schema=schemas.UserCreate,
        update_schema=schemas.UserUpdate,
        db_model=models.User,
        db=get_db,
        tags=['User'],
        prefix='user'
    )
)