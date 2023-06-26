from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, List

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ImageConfirmation(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str

    def __init__(
        self,
        name: _Optional[str] = ...,
    ) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ["URL"]
    URL_FIELD_NUMBER: _ClassVar[int]
    URL: str

    def __init__(
        self,
        URL: _Optional[str] = ...,
    ) -> None: ...

class Transformation(_message.Message):
    __slots__ = ["name", "URL"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    URL: str

    def __init__(
        self,
        name: _Optional[str] = ...,
        URL: _Optional[str] = ...,
    ) -> None: ...

class ModifiedImageResponse(_message.Message):
    __slots__ = ["name", "transformation"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    transformation: List

    def __init__(
        self,
        name: _Optional[str] = ...,
        transformation: _Optional[List] = ...,
    ) -> None: ...
