from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ["name", "confirmation"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    confirmation: bool
    def __init__(
        self, name: _Optional[str] = ..., confirmation: _Optional[bool] = ...
    ) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ["URL"]
    URL_FIELD_NUMBER: _ClassVar[int]
    URL: str

    def __init__(
        self,
        URL: _Optional[str] = ...,
    ) -> None: ...

class ImageModifiedResponse(_message.Message):
    __slots__ = ["name", "image_cropped_URL", "image_BW_URL"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_CROPPED_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BW_URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    image_cropped_URL: str
    image_BW_URL: str

    def __init__(
        self,
        name: _Optional[str] = ...,
        image_cropped_URL: _Optional[str] = ...,
        image_BW_URL: _Optional[str] = ...,
    ) -> None: ...
