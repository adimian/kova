import sqlalchemy as sa
from ulid import ULID as _ULID


class ULID(_ULID):
    def __hash__(self):
        return hash(str(self))


class ULIDType(sa.types.TypeDecorator):
    impl = sa.Unicode
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect) -> ULID | None:
        if value is not None:
            return ULID.from_str(value)
        return None

    @property
    def python_type(self):
        return self.impl.type.python_type
