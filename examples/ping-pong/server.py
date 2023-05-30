"""
    This server serves back messages sent to `*.echo.identified`
    The reply will contain the name of the current user

    $ python scripts/nats-pub.py --request user_ulid.echo.identified

"""

from loguru import logger

from kova.protocol.ping_pb2 import EchoRequest
from kova.server import Server, Router


router = Router()


@router.subscribe("*.ping")
async def ping_pong(msg: EchoRequest):
    logger.debug(f"received message: {msg.message}")


server = Server()
server.add_router(router=router)
server.run()
