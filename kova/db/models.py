from . import Base
from sqlalchemy import Column, String
from ulid import ULID


class User(Base):
    id = Column(String(), default=ULID)
