import sqlite3

from pathlib import Path
from loguru import logger
from typing import List

from kova.our_types import Dependable
from kova.settings import get_settings
from kova.ulid_types import ULID


class DBConnection(object):
    def __init__(self, path):
        try:
            self.connection = sqlite3.connect(path)
            logger.debug("SQLite Connection opened")
        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

    def __enter__(self):
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()
        logger.debug("SQLite Connection closed")


class Buffer(Dependable):
    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self, subject: str):
        settings = get_settings()

        self._path = Path(settings.buffer_database_file) / "buffer.db"
        self.subject = subject.replace(".", "_")

        with DBConnection(self._path) as connection:
            cursor = connection.cursor()
            logger.debug("Buffer DB init")

            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.subject}
                (id CHAR(128), message VARCHAR(255))"""
            )

            cursor.close()

    def save(self, message: bytes) -> str:
        if not isinstance(message, bytes):
            raise TypeError("value must be of type bytes")

        id = ULID()

        with DBConnection(self._path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"""
                INSERT INTO {self.subject}
                (id, message)
                VALUES (?,?)""",
                (str(id), message),
            )

            connection.commit()
            logger.debug("Message saved in buffer")

            cursor.close()

        return str(id)

    def get(self) -> bytes | None:
        with DBConnection(self._path) as connection:
            cursor = connection.cursor()

            request = cursor.execute(
                f"""
                SELECT id, message FROM {self.subject} ORDER BY id ASC
            """
            )

            result = request.fetchone()

            if result is None:
                message = None
            else:
                message = result[1]
                cursor.execute(
                    f"""
                    DELETE FROM {self.subject} WHERE id = ?
                """,
                    (result[0],),
                )

                connection.commit()
                logger.debug("Message fetched from buffer")

            cursor.close()

        return message

    def get_all(self) -> List[bytes] | None:
        with DBConnection(self._path) as connection:
            connection.row_factory = lambda cursor, row: row[0]
            cursor = connection.cursor()

            request = cursor.execute(
                f"""
                SELECT message FROM {self.subject} ORDER BY id ASC
            """
            )

            messages = request.fetchall()
            logger.debug("Message fetched from buffer")

            cursor.execute(
                f"""
                DELETE FROM {self.subject}
            """
            )

            connection.commit()

            cursor.close()

        return messages

    def delete_message(self, id: str):
        with DBConnection(self._path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"SELECT message FROM {self.subject} WHERE id = ?", (id,)
            )
            data = cursor.fetchone()
            if data is None:
                raise ValueError(f"There is no message named {id}")

            cursor.execute(
                f"""
                DELETE FROM {self.subject} WHERE id = ?
            """,
                (id,),
            )

            connection.commit()
            logger.debug("Message deleted from buffer")

            cursor.close()

    def remove(self):
        with DBConnection(self._path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"""
                DELETE FROM {self.subject} ORDER BY id DESC LIMIT 1
            """
            )

            connection.commit()
            logger.debug("Message deleted from buffer")

            cursor.close()


Dependable.register(Buffer)
