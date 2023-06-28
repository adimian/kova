import requests
import os
from enum import Enum

from loguru import logger

from kova.protocol.image_pb2 import (
    ImageRequest,
    ImageResponse,
    ImageConfirmation,
    Crop,
)


class Modes(Enum):
    NONE = ""
    BW = "L"


async def connect(nc, path_file: str, user_name: str):
    path, file = os.path.split(path_file)
    name, ext = file.split(".")

    req = ImageRequest()
    req.name = name
    payload = req.SerializeToString()

    response = await nc.request(f"{user_name}.send_file", payload, timeout=10)
    print(f"Requested on [{user_name}.send_file] : '{file}'")

    res = ImageResponse.FromString(response.data)
    print("Got response with presigned URL")

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
    transformation: str,
    crop: Crop = Crop(),
    color: Modes = Modes.NONE,
):
    req = ImageConfirmation()
    req.name = name
    req.transformation = transformation
    if transformation == "crop":
        print(crop)
        req.crop = crop
    elif transformation == "color":
        req.mode = color.value
    else:
        print("No")
    payload = req.SerializeToString()

    response = await nc.request(
        f"{user_name}.transform_file", payload, timeout=10
    )
    print(f"Requested on [{user_name}.transform_file] : '{name}'")

    res = ImageResponse.FromString(response.data)
    print("Got response with presigned URL")

    request_res = requests.get(res.URL)

    if request_res.status_code == 200:
        return request_res.content
    else:
        logger.debug(request_res.text)


async def crop_image(nc, name: str, user_name: str, dimension):
    crop = Crop()
    crop.left = dimension[0]
    crop.top = dimension[1]
    crop.right = dimension[2]
    crop.bottom = dimension[3]
    image = await modify_image(nc, name, user_name, "crop", crop=crop)
    return image


async def color_image(nc, name: str, user_name: str, mode: Modes):
    image = await modify_image(nc, name, user_name, "color", color=mode)
    return image
