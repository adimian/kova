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
    name = msg.origin.split(".")
    if name[0] == current_user.name:

        logger.debug(
            f"Received message from {current_user.name} to "
            f"{msg.destination}: '{msg.message}'"
        )

        relay = PingRequest()
        subject = f"{msg.destination}.ping"

        relay.destination = msg.destination
        relay.message = msg.message
        relay.origin = current_user.name
        payload = relay.SerializeToString()

        publish = Publish.get_instance(router)
        await publish(subject=subject, payload=payload)
        logger.debug(f"Send message on [{subject}] : '{relay.message}'")


server = Server()
server.add_router(router=router)
server.run()
