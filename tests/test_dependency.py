from kova.cache import Cache
from kova.router import Router


def test_dependency_can_be_registered_in_router():
    router = Router()

    @router.subscribe("test.dependency")
    async def request_cache(cache: Cache):
        if cache is None:
            raise RuntimeError()
