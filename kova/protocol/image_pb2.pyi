from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ["name", "image"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    image: bytes
    def __init__(
        self, name: _Optional[str] = ..., image: _Optional[bytes] = ...
    ) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ["name", "image_cropped", "image_BW"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_CROPPED_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BW_FIELD_NUMBER: _ClassVar[int]
    name: str
    image_cropped: bytes
    image_BW: bytes

    def __init__(
        self,
        name: _Optional[str] = ...,
        image_cropped: _Optional[bytes] = ...,
        image_BW: _Optional[bytes] = ...,
    ) -> None: ...
