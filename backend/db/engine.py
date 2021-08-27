from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True  # https://docs.sqlalchemy.org/en/14/core/pooling.html#dealing-with-disconnects
)

async_session = sessionmaker(
    engine,
    expire_on_commit=True,
    class_=AsyncSession
)
