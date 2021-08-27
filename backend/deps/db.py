import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.engine import async_session


async def get_db() -> AsyncSession:
    session = async_session()
    try:
        yield session
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(e)
    finally:
        await session.close()
