from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AccessTokenRequest(_message.Message):
    __slots__ = ["refresh_token"]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...

class AccessTokenResponse(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ["email", "mfa_code"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    MFA_CODE_FIELD_NUMBER: _ClassVar[int]
    email: str
    mfa_code: str
    def __init__(
        self, email: _Optional[str] = ..., mfa_code: _Optional[str] = ...
    ) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ["refresh_token"]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...
