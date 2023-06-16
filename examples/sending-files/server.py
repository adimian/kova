from kova.protocol.image_pb2 import ImageRequest, ImageResponse
from kova.server import Server, Router
from kova.message import Reply
from kova.current_user import CurrentUser
from kova.settings import get_settings

from minio import Minio
from loguru import logger
from PIL import Image

import io


router = Router()


def image_to_bytes(img: Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), buf.tell()


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
    image = Image.open(io.BytesIO(msg.image))

    image_cropped = image.crop((155, 65, 360, 270))
    image_greyscale = image.convert("L")

    byte_image, image_size = image_to_bytes(image)
    byte_cropped, image_size_cr = image_to_bytes(image_cropped)
    byte_BW, image_size_bw = image_to_bytes(image_greyscale)

    client.put_object(
        current_user.name, msg.name, io.BytesIO(byte_image), image_size
    )
    client.put_object(
        current_user.name,
        f"{msg.name}-cropped",
        io.BytesIO(byte_cropped),
        image_size_cr,
    )
    client.put_object(
        current_user.name, f"{msg.name}-bw", io.BytesIO(byte_BW), image_size_bw
    )

    if reply:
        res = ImageResponse()

        res.name = msg.name
        res.image_cropped = byte_cropped
        res.image_BW = byte_BW

        await reply(res.SerializeToString())
        logger.debug("Response sent")
    else:
        logger.warning("Unable to reply")


server = Server()
server.add_router(router=router)
server.run()
