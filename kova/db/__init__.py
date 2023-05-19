from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.orm import (
    DeclarativeMeta,
    declarative_base,
    Session,
    object_session,
)

from kova.settings import get_settings

_Base: DeclarativeMeta = declarative_base()


class Base(_Base):
    __abstract__ = True

    def _get_object_session(self) -> Session:
        session = object_session(self)
        return session


@lru_cache()
def get_engine() -> AsyncEngine:
    settings = get_settings().database

    engine = create_async_engine(
        settings.uri,
        echo=settings.echo,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.pool_max_overflow,
    )
    return engine


async def get_session():
    session = AsyncSession(get_engine(readonly=False))
    try:
        yield session
    finally:
        await session.close()
