import abc
from collections import deque, defaultdict
from typing import Type, TypeAlias

from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg

from .types import Message, Reply, Publish


class Context:
    pass


class InMemoryQueue:
    def __init__(self):
        self._messages = defaultdict(deque)

    async def messages(self, subject: str):
        while True:
            q = self._messages[subject]
            if q:
                yield q.pop()
            else:
                break

    async def publish(self, subject: str, payload: bytes):
        self._messages[subject].append(payload)


Queue: TypeAlias = NATSClient | InMemoryQueue
MessageType: TypeAlias = Type[Message]


class Handler(abc.ABC):
    def __init__(self, message_type: MessageType):
        self.message_type = message_type

    @abc.abstractmethod
    async def __call__(
        self,
        context: Context,
        message: Message,
        reply: Reply,
        publish: Publish,
    ):
        raise NotImplementedError()


class Route:
    def __init__(
        self,
        name: str | None,
        subject: str,
        message_type: MessageType,
        queue: Queue,
    ):
        self.name = name
        self.subject = subject
        self.message_type = message_type
        self.handlers: list[Handler] = []
        self.queue = queue

    def add_handler(self, handler: Type[Handler]):
        if not issubclass(handler, Handler):
            raise TypeError("handler must be a Handler subclass")
        self.handlers.append(handler(message_type=self.message_type))

    async def __call__(
        self,
        context: Context,
        msg: Msg,
    ):
        message = self.message_type.FromString(msg.data)

        async def publish(subject: str, payload: bytes):
            await self.queue.publish(subject=subject, payload=payload)

        if msg.reply:

            async def reply(payload: bytes):
                await publish(subject=msg.reply, payload=payload)

        else:
            reply = None  # type: ignore

        for handler in self.handlers:
            await handler(
                message=message,
                context=context,
                reply=reply,
                publish=publish,
            )


class Router:
    def __init__(self, queue: Queue | None = None):
        self.routes: list[Route] = []
        self.queue = queue

    def bind(self, queue: Queue):
        self.queue = queue

    def add_route(
        self,
        subject: str,
        message_type: MessageType,
        *,
        name: str | None = None,
    ):
        route = Route(
            queue=self.queue,
            name=name,
            subject=subject,
            message_type=message_type,
        )
        self.routes.append(route)

        return route
