import abc
import dataclasses
from typing import Callable, Awaitable, Optional, TypeAlias, Type

import google.protobuf.message as _message

ReplyType: TypeAlias = Optional[Callable[[bytes], Awaitable[None]]]
PublishType: TypeAlias = Callable[[str, bytes], Awaitable[None]]
Message: TypeAlias = _message.Message


class Dependable(abc.ABC):
    _instances: list[Type["Dependable"]] = []

    @classmethod
    def register(cls, instance: Type["Dependable"]):
        cls._instances.append(instance)

    @classmethod
    def get_instances(cls) -> list[Type["Dependable"]]:
        return cls._instances

    @classmethod
    @abc.abstractmethod
    def get_instance(cls, *, router, subject, msg):
        raise NotImplementedError()


class Publish(Dependable):
    def __call__(self, subject: str, payload: bytes):
        raise NotImplementedError("you should not see this")

    @classmethod
    def get_instance(cls, router, **kwargs):
        async def publish(subject: str, payload: bytes):
            await router.queue.publish(  # type: ignore
                subject=subject, payload=payload
            )

        return publish


Dependable.register(Publish)


class Reply(Dependable):
    def __call__(self, payload: bytes):
        raise NotImplementedError("you should not see this")

    @classmethod
    def get_instance(cls, router, msg, **kwargs):
        if msg.reply:

            async def reply(payload: bytes):
                p = Publish().get_instance(router=router)
                await p(subject=msg.reply, payload=payload)

            return reply
        else:
            return None


Dependable.register(Reply)


@dataclasses.dataclass
class Msg:
    """used in unit-testing context to simulate NATS messages"""

    subject: str = ""
    reply: str = ""
    data: bytes = b""
    headers: dict[str, str] | None = None
