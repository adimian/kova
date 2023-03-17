from typing import Callable, TypeVar, Awaitable, Optional, TypeAlias
import google.protobuf.message as _message

T = TypeVar("T")
Reply = Optional[Callable[[bytes], Awaitable[None]]]
Publish = Callable[[str, bytes], Awaitable[None]]
Message: TypeAlias = _message.Message
