import tempfile
import os
from pathlib import Path
from loguru import logger
from typing import List

from kova.our_types import Dependable
from kova.ulid_types import ULID


class Buffer(Dependable):
    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self, subject: str):
        self.subject = subject

        if not os.path.exists(
            Path(tempfile.gettempdir()) / "messages" / subject
        ):
            os.makedirs(Path(tempfile.gettempdir()) / "messages" / subject)

        self._path: str = (
            Path(tempfile.gettempdir()) / "messages" / subject
        ).as_posix()

    def save(self, message: bytes):

        if not isinstance(message, bytes):
            raise ValueError("value must be of type bytes")

        name = ULID()
        with open(Path(self._path) / f"{name}.bin", "wb") as f:
            f.write(message)
        logger.debug("Message saved in buffer")
        return str(name)

    def get(self) -> bytes | None:
        files_list = os.listdir(Path(self._path))
        if not files_list:
            logger.debug("No messages in buffer")
            return None
        else:
            for file in files_list:
                if file.endswith(".bin"):
                    with open(Path(self._path) / file, "rb") as f:
                        message = f.read()
                    os.remove(Path(self._path) / file)
                    logger.debug("Got message from buffer")
                    return message
            logger.debug("No messages in buffer")
            return None

    def get_all(self) -> List[bytes] | None:
        messages = []
        files_list = os.listdir(Path(self._path))
        if not files_list:
            logger.debug("No messages in buffer")
            return None
        else:
            for file in files_list:
                if file.endswith(".bin"):
                    with open(Path(self._path) / file, "rb") as f:
                        message = f.read()
                    os.remove(Path(self._path) / file)
                    messages.append(message)
            return messages

    def remove(self, name: str):
        os.remove(Path(self._path) / f"{name}.bin")
        logger.debug("Message sent and removed from buffer")


Dependable.register(Buffer)
