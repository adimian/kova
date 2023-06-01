from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ["destination", "message"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    destination: str
    message: str
    def __init__(
        self, destination: _Optional[str] = ..., message: _Optional[str] = ...
    ) -> None: ...

class PongResponse(_message.Message):
    __slots__ = ["destination", "message"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    destination: str
    message: str

    def __init__(
        self, destination: _Optional[str] = ..., message: _Optional[str] = ...
    ) -> None: ...
