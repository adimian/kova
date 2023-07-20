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
        return str(name)

    def get(self, subject: str) -> bytes | None:
        subject = subject.replace(".", "_")

        if not os.path.exists(Path(self._path) / subject):
            return None

        files_list = os.listdir(Path(self._path) / subject)
        if not files_list:
            logger.debug("No messages in buffer")
            return None
        else:
            for file in files_list:
                if file.endswith(".bin"):
                    with open(Path(self._path) / subject / file, "rb") as f:
                        message = f.read()
                    os.remove(Path(self._path) / subject / file)
                    logger.debug("Got message from buffer")
                    return message
            return None

    def remove(self, subject: str, name: str):
        subject = subject.replace(".", "_")

        os.remove(Path(self._path) / subject / f"{name}.bin")
        logger.debug("Message sent and removed from buffer")


Dependable.register(Buffer)
