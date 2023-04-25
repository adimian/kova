from sqlalchemy import Column, String

from . import Base
from ..types import ULIDType, ULID


class User(Base):
    __tablename__ = "auth_users"
    id = Column(ULIDType(), default=ULID, primary_key=True)
    email = Column(String())
