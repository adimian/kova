import pytest

from kova.authentication.nsc_wrapper import NscWrapper, NscException


def test_nsc_wrapper_can_return_nsc_version():
    nsc = NscWrapper(nsc_path="nsc")
    version = nsc.get_version()
    assert version.startswith("nsc version")


def test_nsc_wrapper_throws_exception_when_nsc_not_available():
    nsc = NscWrapper(nsc_path="not-nsc")
    with pytest.raises(NscException):
        nsc.get_version()
