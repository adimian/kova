import dataclasses

from arrow import Arrow, now

from kova.types import Dependable


@dataclasses.dataclass
class CacheEntry:
    payload: bytes
    expire_at: Arrow | None


class Cache(Dependable):
    @classmethod
    def get_instance(cls, *, router, subject, msg):
        return cls()

    def __init__(self):
        self._entries: dict[str, CacheEntry] = {}

    async def set(self, key: str, value: bytes, ttl: float | None = None):
        if ttl is not None:
            if ttl <= 0:
                raise ValueError("TTL must be a strictly positive float")
            expire_at = now().shift(seconds=ttl)
        else:
            expire_at = None

        if not isinstance(key, str):
            raise ValueError("key must be of type str")  # pragma: no cover

        if not isinstance(value, bytes):
            raise ValueError("value must be of type bytes")  # pragma: no cover

        self._entries[key] = CacheEntry(
            payload=value,
            expire_at=expire_at,
        )

    async def get(self, key: str) -> bytes | None:
        entry = self._entries.get(key)
        if entry is not None and (
            entry.expire_at is None or entry.expire_at >= now()
        ):
            return entry.payload
        else:
            return None


Dependable.register(Cache)
