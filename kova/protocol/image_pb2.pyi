from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, List, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Crop(_message.Message):
    __slots__ = ["left", "top", "right", "bottom"]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    left: int
    top: int
    right: int
    bottom: int

    def __init__(
        self,
        left: _Optional[int] = ...,
        top: _Optional[int] = ...,
        right: _Optional[int] = ...,
        bottom: _Optional[int] = ...,
    ) -> None: ...

class ImageRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ImageConfirmation(_message.Message):
    __slots__ = ["name", "transformation", "crop", "mode"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    CROP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    name: str
    transformation: str
    crop: Crop
    mode: str

    def __init__(
        self,
        name: _Optional[str] = ...,
        transformation: _Optional[str] = ...,
        crop: _Optional[Crop] = ...,
        mode: _Optional[str] = ...,
    ) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ["URL"]
    URL_FIELD_NUMBER: _ClassVar[int]
    URL: str

    def __init__(
        self,
        URL: _Optional[str] = ...,
    ) -> None: ...
