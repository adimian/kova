import tempfile
import os
from pathlib import Path
from loguru import logger

from kova.our_types import Dependable
from kova.ulid_types import ULID


class Buffer(Dependable):
    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self):
        self._path: str = (Path(tempfile.gettempdir()) / "messages").as_posix()

    def save(self, message: bytes, subject: str):
        name = ULID()
        subject = subject.replace(".", "_")
        if not os.path.exists(Path(self._path) / subject):
            os.makedirs(Path(self._path) / subject)
        with open(Path(self._path) / subject / f"{name}.bin", "wb") as f:
            f.write(message)
        logger.debug("Message saved in buffer")

    def get(self, subject: str) -> bytes | None:
        subject = subject.replace(".", "_")
        if not os.path.exists(Path(self._path) / subject):
            return None
        files_list = os.listdir(Path(self._path) / subject)
        if not files_list:
            logger.debug("No messages in buffer")
            return None
        else:
            logger.debug(files_list[0])
            with open(Path(self._path) / subject / files_list[0], "rb") as f:
                message = f.read()
            os.remove(Path(self._path) / subject / files_list[0])
            logger.debug("Got message from buffer")
            return message

    def remove(self, subject: str):
        subject = subject.replace(".", "_")
        files_list = os.listdir(Path(self._path) / subject)
        if len(files_list) == 1:
            os.remove(Path(self._path) / subject / files_list[0])
            logger.debug("Message sent and removed from buffer")
        else:
            logger.debug("Problem")


Dependable.register(Buffer)
