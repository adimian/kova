from kova.protocol.image_pb2 import ImageRequest
from kova.server import Server, Router
from kova.message import Reply
from kova.current_user import CurrentUser
from kova.settings import get_settings

from minio import Minio
from loguru import logger


router = Router()


@router.subscribe("*.send_file")
async def file_request(
    msg: ImageRequest, current_user: CurrentUser, reply: Reply
):
    settings = get_settings()

    client = Minio(
        settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )

    found = client.bucket_exists(current_user.name)
    if not found:
        client.make_bucket(current_user.name)
    else:
        logger.debug(f"Bucket {current_user.name} already exists")

    logger.debug(f"message : {msg.name}")


server = Server()
server.add_router(router=router)
server.run()
