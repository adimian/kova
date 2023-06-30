from typing import List

import requests
import os
from enum import Enum

from loguru import logger

from PIL import Image
from pathlib import Path

import io

from kova.protocol.image_pb2 import (
    ImageRequest,
    ImageResponse,
    ImageConfirmation,
)


class Modes(Enum):
    NONE = ""
    BW = "BW"
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"


async def connect(nc, path_file: str, user_name: str):
    path, file = os.path.split(path_file)
    name, ext = file.split(".")

    req = ImageRequest()
    req.name = name
    payload = req.SerializeToString()

    response = await nc.request(f"{user_name}.send_file", payload, timeout=10)
    logger.debug(f"Requested on [{user_name}.send_file] : '{file}'")

    res = ImageResponse.FromString(response.data)
    logger.debug("Got response with presigned URL")

    # Upload image with presigned URL
    with open(path_file, mode="rb") as f:
        byte_im = f.read()

    request_res = requests.put(res.URL, data=byte_im)

    if request_res.status_code == 200:
        logger.debug("Image sent")
    else:
        logger.debug(request_res.text)


async def modify_image(
    nc,
    name: str,
    user_name: str,
    req: ImageConfirmation,
):
    payload = req.SerializeToString()

    response = await nc.request(
        f"{user_name}.transform_file", payload, timeout=10
    )
    logger.debug(f"Requested on [{user_name}.transform_file] : '{name}'")

    res = ImageResponse.FromString(response.data)
    logger.debug("Got response with presigned URL")

    request_res = requests.get(res.URL)

    if request_res.status_code == 200:
        return request_res.content
    else:
        logger.debug(request_res.text)


async def crop_image(nc, name: str, user_name: str, dimension: List[int]):
    req = ImageConfirmation()
    req.name = name
    req.transformation = "crop"
    req.crop.left = dimension[0]
    req.crop.top = dimension[1]
    req.crop.right = dimension[2]
    req.crop.bottom = dimension[3]

    image = await modify_image(nc, name, user_name, req)
    return image


async def color_image(nc, name: str, user_name: str, mode: Modes):
    req = ImageConfirmation()
    req.name = name
    req.transformation = "color"
    req.mode = mode.value

    image = await modify_image(nc, name, user_name, req)
    return image


def save_image(image, path, name):
    image_save = Image.open(io.BytesIO(image))
    image_save.save(Path(path) / f"{name}.png", "png", quality="keep")
    image_save.show()
