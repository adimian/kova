"""
    This server serves back messages sent to `*.echo.identified`
    The reply will contain the name of the current user

    $ python scripts/nats-pub.py --request user_ulid.echo.identified

"""

from loguru import logger

from kova.protocol.ping_pb2 import EchoRequest, EchoResponse
from kova.server import Server, Router
from kova.current_user import CurrentUser
from kova.message import Reply


router = Router()


@router.subscribe("*.echo.identified")
async def identified_request(
    msg: EchoRequest, current_user: CurrentUser, reply: Reply
):
    logger.debug(f"Received message: '{msg.message}'")
    if reply:
        res = EchoResponse()
        res.message = f"echo {msg.message} from {current_user.name}"
        await reply(res.SerializeToString())
        logger.debug("Response sent")
    else:
        logger.warning("Unable to reply")


server = Server()
server.add_router(router=router)
server.run()
