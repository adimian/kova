import dataclasses
from typing import Callable, Awaitable, Optional, TypeAlias

import google.protobuf.message as _message

ReplyType: TypeAlias = Optional[Callable[[bytes], Awaitable[None]]]
PublishType: TypeAlias = Callable[[str, bytes], Awaitable[None]]
Message: TypeAlias = _message.Message


class Publish:
    def __call__(self, subject: str, payload: bytes):
        raise NotImplementedError("you should not see this")


class Reply:
    def __call__(self, payload: bytes):
        raise NotImplementedError("you should not see this")


@dataclasses.dataclass
class Msg:
    """used in unit-testing context to simulate NATS messages"""

    subject: str = ""
    reply: str = ""
    data: bytes = b""
    headers: dict[str, str] | None = None
