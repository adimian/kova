import pytest
from loguru import logger

from kova.authentication.nsc import NscWrapper, NscException


@pytest.fixture()
def nsc(tmp_path):
    return NscWrapper(
        nsc_path="nsc",
        data_dir=(tmp_path / "stores").as_posix(),
        keystore_dir=(tmp_path / "keys").as_posix(),
    )


def test_nsc_wrapper_can_return_nsc_version(tmp_path):
    nsc = NscWrapper(
        nsc_path="nsc",
        data_dir=(tmp_path / "stores").as_posix(),
        keystore_dir=(tmp_path / "keys").as_posix(),
    )
    version = nsc.get_version()
    logger.debug(version)
    assert version.startswith("nsc version")


def test_nsc_wrapper_throws_exception_when_nsc_not_available(tmp_path):
    nsc = NscWrapper(
        nsc_path="not-nsc",
        data_dir=(tmp_path / "stores").as_posix(),
        keystore_dir=(tmp_path / "keys").as_posix(),
    )
    with pytest.raises(NscException):
        nsc.get_version()


def test_nsc_can_create_an_operator(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    jwt = nsc.get_operator_jwt(name="bobby")
    assert jwt.count(".") == 2


def test_nsc_can_create_an_account(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    nsc.create_account(name="bob")
    jwt = nsc.get_account_jwt(name="bob")
    assert jwt.count(".") == 2


def test_nsc_can_create_a_user(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    nsc.create_account(name="bob")

    nsc.create_user(name="bo")
    jwt = nsc.get_user_jwt(name="bo")
    assert jwt.count(".") == 2


def test_nsc_can_create_a_user_with_permission(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    nsc.create_account(name="bob")

    nsc.create_user(
        name="bo", allow_pub="bo.>", allow_sub="_INBOX.>", expiry="6M"
    )
    jwt = nsc.get_user_jwt(name="bo")
    logger.debug(jwt)
    assert jwt.count(".") == 2


def test_nsc_can_create_a_user_with_some_permission(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    nsc.create_account(name="bob")

    nsc.create_user(name="bo", allow_pub="bo.>", allow_sub="_INBOX.>")
    jwt = nsc.get_user_jwt(name="bo")
    logger.debug(jwt)
    assert jwt.count(".") == 2


def test_nsc_can_create_a_user_with_wrong_permission(nsc: NscWrapper):
    nsc.create_operator(name="bobby")

    nsc.create_account(name="bob")

    with pytest.raises(NscException):
        nsc.create_user(name="bo", not_allow_pub="bo.>", allow_sub="_INBOX.>")
