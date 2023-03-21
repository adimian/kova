import asyncio
import signal
import sys

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

    async def start(self, aloop):
        async def error_cb(e):
            logger.error("Error:", e)

        async def closed_cb():
            logger.info("Connection to NATS is closed.")
            await asyncio.sleep(0.1)
            aloop.stop()

        async def reconnected_cb():
            logger.info(
                f"Connected to NATS at {self.queue.connected_url.netloc}..."
            )

        options = {
            "error_cb": error_cb,
            "closed_cb": closed_cb,
            "reconnected_cb": reconnected_cb,
            "servers": self.settings.nats_servers,
        }

        await self.queue.connect(**options)

        for subject, handlers in self.router.handlers.items():
            for handler in handlers:
                logger.info(f"Added subscription for {subject=} to {handler=}")
                await self.queue.subscribe(subject=subject, cb=handler)

        def signal_handler():
            if self.queue.is_closed:
                return
            logger.warning("Disconnecting...")
            aloop.create_task(self.queue.close())
            sys.exit(1)

        for sig in ("SIGINT", "SIGTERM"):
            aloop.add_signal_handler(getattr(signal, sig), signal_handler)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    server = Server(settings=get_settings())
    loop.run_until_complete(server.start(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
