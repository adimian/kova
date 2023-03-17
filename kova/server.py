from nats.aio.client import Client as NatsClient

from kova.router import Router, Context
from kova.settings import Settings


class Server:
    def __init__(
        self,
        settings: Settings,
        *,
        queue: NatsClient | None = None,
        router: Router | None = None,
        context: Context | None = None,
    ):
        self.settings = settings
        self.queue = queue or NatsClient(settings.nats_servers)
        self.registry = router or Router()
        self.context = context or Context()
