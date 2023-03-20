import time

import pytest

from kova.cache import Cache


def test_cache_can_set_and_get_value():
    c = Cache()
    c.set("greetings", b"hello")
    assert c.get("greetings")


def test_cache_can_set_value_with_a_ttl():
    c = Cache()
    c.set("greetings", b"hello", ttl=0.1)
    assert c.get("greetings") == b"hello"
    time.sleep(0.5)
    assert c.get("greetings") is None


def test_cache_ttl_value_cannot_be_negative_or_zero():
    c = Cache()
    with pytest.raises(ValueError):
        c.set("greetings", b"hello", ttl=0)

    with pytest.raises(ValueError):
        c.set("greetings", b"hello", ttl=-1)
