import sqlite3

from pathlib import Path
from loguru import logger
from typing import List

from kova.our_types import Dependable
from kova.settings import get_settings
from kova.ulid_types import ULID


class Buffer(Dependable):
    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self, subject: str):
        settings = get_settings()

        self._path = Path(settings.buffer_database_file) / "sql.db"
        self.subject = subject.replace(".", "_")

        try:
            connexion = sqlite3.connect(self._path)
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.subject}
                (name VARCHAR(255), message VARCHAR(255))"""
            )

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")

        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

    def save(self, message: bytes) -> str:

        if not isinstance(message, bytes):
            raise TypeError("value must be of type bytes")

        name = ULID()

        try:
            connexion = sqlite3.connect(self._path)
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            cursor.execute(
                f"""
                INSERT INTO {self.subject}
                (name, message)
                VALUES (?,?)""",
                (str(name), message),
            )

            connexion.commit()
            logger.debug("Message saved in buffer")

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")

        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

        return str(name)

    def get(self) -> bytes | None:
        try:
            connexion = sqlite3.connect(self._path)
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            requete = cursor.execute(
                f"""
                SELECT name, message FROM {self.subject} ORDER BY name ASC
            """
            )

            name, message = requete.fetchone()

            cursor.execute(
                f"""
                DELETE FROM {self.subject} WHERE name LIKE ?
            """,
                (name,),
            )

            connexion.commit()
            logger.debug("Message deleted from buffer")

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")

        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

        return message

    def get_all(self) -> List[bytes] | None:
        try:
            connexion = sqlite3.connect(self._path)
            connexion.row_factory = lambda cursor, row: row[0]
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            requete = cursor.execute(
                f"""
                SELECT message FROM {self.subject} ORDER BY name ASC
            """
            )

            messages = requete.fetchall()
            logger.debug("Message saved in buffer")

            cursor.execute(
                f"""
                DELETE FROM {self.subject}
            """
            )

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")

        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

        return messages

    def delete_message(self, name: str):
        try:
            connexion = sqlite3.connect(self._path)
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            cursor.execute(
                f"SELECT * FROM {self.subject} WHERE name = ?", (name,)
            )
            data = cursor.fetchone()
            if data is None:
                raise ValueError(f"There is no message named {name}")

            cursor.execute(
                f"""
                DELETE FROM {self.subject} WHERE name LIKE ?
            """,
                (name,),
            )

            connexion.commit()
            logger.debug("Message deleted from buffer")

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")

        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

    def remove(self):
        # TODO : remove oldest message
        try:
            connexion = sqlite3.connect(self._path)
            cursor = connexion.cursor()
            logger.debug("Buffer DB init")

            cursor.execute(
                f"""
                DELETE FROM {self.subject}
            """
            )

            connexion.commit()
            logger.debug("Message deleted from buffer")

            cursor.close()

            connexion.close()
            logger.debug("SQLite Connection closed")
        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)


Dependable.register(Buffer)
