import pytest

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
