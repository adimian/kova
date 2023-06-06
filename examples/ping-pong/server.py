"""
    This server serves back messages sent to `*.echo.identified`
    The reply will contain the name of the current user

    $ python scripts/nats-pub.py --request user_ulid.echo.identified

"""

from loguru import logger

from kova.current_user import CurrentUser
from kova.protocol.pingpong_pb2 import PingRequest
from kova.server import Server, Router
from kova.message import Publish


router = Router()


@router.subscribe("*.ping")
async def ping_pong(msg: PingRequest, current_user: CurrentUser):
    if msg.original:
        logger.debug(f"received message: {msg.message} for {msg.destination}")

        relay = PingRequest()
        subject = f"{msg.destination}.ping"

        relay.destination = current_user.name
        relay.original = False
        relay.message = msg.message
        payload = relay.SerializeToString()

        publish = Publish.get_instance(router)
        await publish(subject=subject, payload=payload)
    else:
        logger.debug("Relay message not processed")


server = Server()
server.add_router(router=router)
server.run()
