import warnings
from collections import deque, defaultdict
from typing import Type, TypeAlias, Callable, Any

from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg as NATSMsg
from nats.js.client import JetStreamContext as JetStreamClient

from .our_types import Message, Dependable
from .current_user import CurrentUser


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


Queue: TypeAlias = NATSClient | JetStreamClient | InMemoryQueue
MessageType: TypeAlias = Type[Message]


class Router:
    def __init__(self, queue: Queue | None = None):
        self.handlers: dict[str, list[Callable]] = defaultdict(list)
        self.queue = queue

    def __repr__(self):
        return f"<Router handlers: {len(self.handlers)}>"

    def add_router(self, router: "Router"):
        router.bind(queue=self.queue)
        for route, handlers in router.handlers.items():
            self.handlers[route].extend(handlers)

    def bind(self, queue: Queue):
        self.queue = queue

    async def dispatch(self, msg: NATSMsg, subject: str):
        if self.queue is None:
            raise RuntimeError("Router not bound to a queue")

        current_user = CurrentUser()
        message_parsed_as = None
        dependencies = tuple(Dependable.get_instances())

        for handler in self.handlers.get(subject, []):
            kwargs: dict[str, Any] = {}

            attr: str
            atype: type

            for attr, atype in handler.__annotations__.items():
                if issubclass(atype, Message):
                    if message_parsed_as:
                        warnings.warn(  # pragma: no cover
                            f"There is only one message per handler call, "
                            f"and {message_parsed_as} has already "
                            f"been defined as the unmarshalling type. "
                            f"You might want to check if "
                            f"using {atype} is also necessary."
                        )
                    else:
                        message_parsed_as = atype
                    message = atype.FromString(msg.data)
                    kwargs[attr] = message
                elif issubclass(atype, CurrentUser):
                    name = msg.subject.split(".")
                    current_user.name = name[0]
                    kwargs[attr] = current_user
                elif issubclass(atype, dependencies):
                    kwargs[attr] = atype.get_instance(  # type: ignore
                        router=self,
                        subject=subject,
                        msg=msg,
                    )

            await handler(**kwargs)

    def subscribe(self, subject: str):
        def wrapper(func):
            for attr, atype in func.__annotations__.items():
                pass  # we could perform some checks here

            self.handlers[subject].append(func)
            return func

        return wrapper
