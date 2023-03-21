import asyncio

from nats.aio.client import Client as NatsClient
from loguru import logger
from kova.router import Router
from kova.settings import Settings, get_settings


class Server:
    def __init__(
        self,
        settings: Settings,
        *,
        queue: NatsClient | None = None,
        router: Router | None = None,
    ):
        self.settings = settings
        self.queue = queue or NatsClient()
        self.router = router or Router(queue=queue)

        logger.success(f"Server started {self.queue=} {self.router=}")

    async def start(self):
        await self.queue.connect(servers=self.settings.nats_servers)
        logger.info("Connected to queue")

        for subject, handlers in self.router.handlers.items():
            for handler in handlers:
                logger.info(f"Added subscription for {subject=} to {handler=}")
                await self.queue.subscribe(subject=subject, cb=handler)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    server = Server(settings=get_settings())
    loop.run_until_complete(server.start())
    try:
        loop.run_forever()
    finally:
        loop.close()
