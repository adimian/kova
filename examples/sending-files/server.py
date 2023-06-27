from datetime import timedelta

from kova.protocol.image_pb2 import (
    ImageRequest,
    ImageResponse,
    ModifiedImageResponse,
    ImageConfirmation,
    Transformation,
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
router_transform = Router()


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
    logger.debug("Response presigned URL sent")


@router_transform.subscribe("*.transform_file")
async def file_transform(
    msg: ImageConfirmation, current_user: CurrentUser, reply: Reply
):
    settings = get_settings()

    client = Minio(
        settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )

    try:
        response = client.get_object(current_user.name, f"{msg.name}.png")

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

        res = ModifiedImageResponse()

        transformation_crop = Transformation()
        transformation_crop.name = "image_cropped"
        transformation_crop.URL = client.presigned_get_object(
            current_user.name,
            f"{msg.name}-cropped.png",
            expires=timedelta(hours=2),
        )

        res.transformation.append(transformation_crop)

        transformation_bw = Transformation()
        transformation_bw.name = "image_greyscale"
        transformation_bw.URL = client.presigned_get_object(
            current_user.name,
            f"{msg.name}-BW.png",
            expires=timedelta(hours=2),
        )

        res.transformation.append(transformation_bw)

        res.name = msg.name

        await reply(res.SerializeToString())
        logger.debug("Response modified images sent")

    except S3Error as exception:
        raise MinioException(exception)


server = Server()
server.add_router(router=router)
server.add_router(router=router_transform)
server.run()
