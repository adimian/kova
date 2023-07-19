import tempfile
import time
import os
from pathlib import Path
from loguru import logger

from kova.our_types import Dependable


class Buffer(Dependable):
    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self):
        self._path: str = (Path(tempfile.gettempdir()) / "messages").as_posix()

    def set(self, message: bytes):
        name = int(time.time())
        with open(Path(self._path) / f"{name}.bin", "wb") as f:
            f.write(message)
        logger.debug("Message saved in buffer")

    def get(self) -> bytes | None:
        filesList = os.listdir(self._path)
        if len(filesList) == 0:
            logger.debug("No messages in buffer")
            return None
        else:
            logger.debug(filesList[0])
            with open(Path(self._path) / filesList[0], "rb") as f:
                message = f.read()
            os.remove(Path(self._path) / filesList[0])
            logger.debug("Got message from buffer")
            return message

    def remove(self):
        filesList = os.listdir(self._path)
        if len(filesList) == 1:
            os.remove(Path(self._path) / filesList[0])
            logger.debug("Message sent and removed from buffer")
        else:
            logger.debug("Problem")


Dependable.register(Buffer)
