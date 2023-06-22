from datetime import timedelta

from kova.protocol.image_pb2 import (
    ImageRequest,
    ImageResponse,
    ImageModifiedResponse,
)
from kova.server import Server, Router
from kova.message import Reply
from kova.current_user import CurrentUser
from kova.settings import get_settings

from minio import Minio
from minio.error import S3Error
from loguru import logger
from PIL import Image
from pathlib import Path

import io


class MinioException(Exception):
    pass


router = Router()


def image_to_bytes(img: Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), buf.tell()


def save_image(client: Minio, image: Image, path: str, name: str, user: str):
    image.save(Path(path) / name, "png", quality="keep")
    byte_image, image_size = image_to_bytes(image)
    client.put_object(user, name, io.BytesIO(byte_image), image_size)


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

    if msg.confirmation:
        try:
            response = client.get_object(current_user.name, f"{msg.name}.png")
        except S3Error as exception:
            raise MinioException(exception)

        image = Image.open(io.BytesIO(response.data))

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

        res = ImageModifiedResponse()

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
        logger.debug("Response for image modified sent")

    else:
        found = client.bucket_exists(current_user.name)
        if not found:
            client.make_bucket(current_user.name)
        else:
            logger.debug(f"Bucket {current_user.name} already exists")

        URL = client.presigned_put_object(
            current_user.name, f"{msg.name}.png", expires=timedelta(hours=2)
        )

        response = ImageResponse()
        response.URL = URL
        await reply(response.SerializeToString())
        logger.debug("Response for initial thingy sent")


server = Server()
server.add_router(router=router)
server.run()
