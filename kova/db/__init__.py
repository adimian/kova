import contextlib
from functools import lru_cache
from typing import Generator

from sqlalchemy import Engine, create_engine
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
def get_engine(readonly: bool = False) -> Engine:
    settings = get_settings().database

    kwargs = {}
    if "sqlite" in settings.uri:
        kwargs["connect_args"] = {"check_same_thread": False}  # type: ignore
    else:
        if readonly:
            kwargs["execution_options"] = {
                "isolation_level": "SERIALIZABLE",  # type: ignore
                "postgresql_readonly": True,
                "postgresql_deferrable": True,
            }

    engine = create_engine(
        settings.uri,
        echo=settings.echo,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.pool_max_overflow,
        **kwargs
    )
    return engine


def get_session(readonly: bool = False) -> Generator[Session, None, None]:
    db = Session(bind=get_engine(readonly=readonly))
    with contextlib.closing(db):
        yield db
