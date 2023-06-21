from datetime import timedelta

from kova.protocol.image_pb2 import ImageRequest, ImageResponse
from kova.server import Server, Router
from kova.message import Reply
from kova.current_user import CurrentUser
from kova.settings import get_settings

from minio import Minio
from loguru import logger
from PIL import Image
from pathlib import Path

import io


router = Router()


def save_image(client: Minio, image: Image, path: str, name: str, user: str):
    image.save(Path(path) / name, "png", quality="keep")
    client.fput_object(user, name, Path(path) / name)


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
    save_image(
        client,
        image,
        settings.minio.temp_path,
        f"{msg.name}.png",
        current_user.name,
    )

    image_cropped = image.crop((155, 65, 360, 270))
    save_image(
        client,
        image_cropped,
        settings.minio.temp_path,
        f"{msg.name}-cropped.png",
        current_user.name,
    )

    image_greyscale = image.convert("L")
    save_image(
        client,
        image_greyscale,
        settings.minio.temp_path,
        f"{msg.name}-BW.png",
        current_user.name,
    )

    if reply:
        res = ImageResponse()

        res.name = msg.name
        res.image_cropped_URL = client.get_presigned_url(
            "GET",
            current_user.name,
            f"{msg.name}-cropped.png",
            expires=timedelta(hours=2),
        )

        res.image_BW_URL = client.get_presigned_url(
            "GET",
            current_user.name,
            f"{msg.name}-bw.png",
            expires=timedelta(hours=2),
        )

        await reply(res.SerializeToString())
        logger.debug("Response sent")
    else:
        logger.warning("Unable to reply")


server = Server()
server.add_router(router=router)
server.run()
