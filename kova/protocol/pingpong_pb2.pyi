from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ["destination", "origin", "message"]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    destination: str
    origin: str
    message: str

    def __init__(
        self,
        destination: _Optional[str] = ...,
        origin: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...
