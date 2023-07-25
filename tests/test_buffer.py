from kova.message_buffer import Buffer

import pytest


def test_buffer_can_save_and_get_message():
    b = Buffer(subject="test.greeting")
    b.save(b"hello")
    assert b.get() == b"hello"


def test_buffer_can_save_and_remove_message():
    b = Buffer(subject="test.greeting")
    name = b.save(b"hello there")
    b.delete_message(name)
    assert b.get() is None


def test_buffer_get_oldest_messages_first():
    b = Buffer(subject="test.greeting")
    b.save(b"hi")
    b.save(b"hello")
    assert b.get() == b"hi"
    assert b.get() == b"hello"


def test_buffer_get_different_message_for_subject():
    b = Buffer(subject="test.greeting")
    c = Buffer(subject="test.greeting.bis")
    b.save(b"hi")
    c.save(b"hello")
    assert b.get() == b"hi"
    assert c.get() == b"hello"


def test_buffer_can_not_get_message_not_sent():
    b = Buffer(subject="test.greeting")
    assert b.get() is None


def test_buffer_object_must_be_bytes():
    b = Buffer(subject="test.greeting")
    with pytest.raises(TypeError):
        b.save("hi")


def test_buffer_cant_delete_message_that_dont_exist():
    b = Buffer(subject="test.greeting")
    with pytest.raises(ValueError):
        b.delete_message("test")


def test_buffer_remove_new_element():
    b = Buffer(subject="test.greeting")
    b.save(b"hi")
    b.save(b"hello")
    b.remove()
    assert b.get() == b"hi"


def test_buffer_get_all_messages_from_oldest():
    b = Buffer(subject="test.greeting")
    b.save(b"hi")
    b.save(b"hello")
    messages = b.get_all()
    print(messages)
    assert messages[0] == b"hi"
