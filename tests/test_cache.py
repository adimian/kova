import time

import pytest

from kova.cache import Cache


@pytest.mark.asyncio
async def test_cache_can_set_and_get_value():
    c = Cache()
    await c.set("greetings", b"hello")
    assert await c.get("greetings")


@pytest.mark.asyncio
async def test_cache_can_set_value_with_a_ttl():
    c = Cache()
    await c.set("greetings", b"hello", ttl=0.1)
    assert await c.get("greetings") == b"hello"
    time.sleep(0.5)
    assert await c.get("greetings") is None


@pytest.mark.asyncio
async def test_cache_ttl_value_cannot_be_negative_or_zero():
    c = Cache()
    with pytest.raises(ValueError):
        await c.set("greetings", b"hello", ttl=0)

    with pytest.raises(ValueError):
        await c.set("greetings", b"hello", ttl=-1)
