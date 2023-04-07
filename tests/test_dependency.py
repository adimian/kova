from kova.cache import Cache
from kova.router import Router
from kova.types import Msg
import pytest


@pytest.mark.asyncio
async def test_dependency_can_be_registered_in_router(queue):
    router = Router(queue=queue)

    @router.subscribe("test.dependency")
    async def request_cache(cache: Cache):
        assert cache is not None

    await router.dispatch(
        subject="test.dependency",
        msg=Msg(
            data=b"",
            subject="test.handler",
        ),
    )
