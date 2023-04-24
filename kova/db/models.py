from . import Base
from sqlalchemy import Column, String
from ulid import ULID


class User(Base):
    __tablename__ = "auth_users"
    id = Column(String(), default=ULID, primary_key=True)
    email = Column(String())
