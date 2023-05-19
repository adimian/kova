import asyncio
import functools
import signal
import sys

from nats.aio.client import Client as NatsClient
from loguru import logger
from kova.router import Router
from kova.settings import Settings, get_settings

from kova import echo

import argparse


class Server:
    def __init__(
        self,
        settings: Settings | None = None,
        *,
        queue: NatsClient | None = None,
        router: Router | None = None,
    ):
        self.settings = settings or get_settings()
        self.queue = queue or NatsClient()
        self.router = router or Router(queue=self.queue)

    def add_router(self, router: Router):
        self.router.add_router(router=router)

    async def start(self, aloop):
        if self.router.queue is None:
            raise RuntimeError("Router not bound to a queue")

        param = argparse.ArgumentParser()
        param.add_argument(
            "--creds",
            type=str,
            default="",
            help="The path to the credential file on your computer",
        )
        param.add_argument(
            "--queue",
            type=str,
            default="echo",
            help="The name of the queue you want to use",
        )
        opt = param.parse_args()

        if opt.queue == "echo":
            self.router.add_router(router=echo.router)

        async def error_cb(e):
            logger.error(f"Error: {e}")

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
            "user_credentials": opt.creds,
        }

        await self.queue.connect(**options)

        for subject in self.router.handlers:
            handler = functools.partial(self.router.dispatch, subject=subject)
            await self.queue.subscribe(subject=subject, cb=handler)

        def signal_handler():
            if self.queue.is_closed:
                return
            logger.warning("Disconnecting...")
            aloop.create_task(self.queue.close())
            sys.exit(1)

        for sig in ("SIGINT", "SIGTERM"):
            aloop.add_signal_handler(getattr(signal, sig), signal_handler)

        logger.success(f"Server started {self.queue=} {self.router=}")

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.start(loop))
        try:
            loop.run_forever()
        finally:
            loop.close()
