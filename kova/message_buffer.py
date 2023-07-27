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

    def _create_connexion(self):
        connexion = None
        try:
            connexion = sqlite3.connect(self._path)
        except sqlite3.Error as error:
            logger.error("Error occurred - ", error)

        return connexion

    def save(self, message: bytes) -> str:
        if not isinstance(message, bytes):
            raise TypeError("value must be of type bytes")

        name = ULID()

        connexion = self._create_connexion()
        cursor = connexion.cursor()

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

        return str(name)

    def get(self) -> bytes | None:
        connexion = self._create_connexion()
        cursor = connexion.cursor()

        requete = cursor.execute(
            f"""
            SELECT name, message FROM {self.subject} ORDER BY name ASC
        """
        )

        result = requete.fetchone()

        if result is None:
            message = None
        else:
            message = result[1]
            cursor.execute(
                f"""
                DELETE FROM {self.subject} WHERE name LIKE ?
            """,
                (result[0],),
            )

            connexion.commit()
            logger.debug("Message fetched from buffer")

        cursor.close()
        connexion.close()

        return message

    def get_all(self) -> List[bytes] | None:
        connexion = self._create_connexion()
        connexion.row_factory = lambda cursor, row: row[0]
        cursor = connexion.cursor()

        requete = cursor.execute(
            f"""
            SELECT message FROM {self.subject} ORDER BY name ASC
        """
        )

        messages = requete.fetchall()
        logger.debug("Message fetched from buffer")

        cursor.execute(
            f"""
            DELETE FROM {self.subject}
        """
        )

        connexion.commit()

        cursor.close()
        connexion.close()

        return messages

    def delete_message(self, name: str):
        connexion = self._create_connexion()
        cursor = connexion.cursor()

        cursor.execute(f"SELECT * FROM {self.subject} WHERE name = ?", (name,))
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

    def remove(self):
        connexion = self._create_connexion()
        cursor = connexion.cursor()

        cursor.execute(
            f"""
            DELETE FROM {self.subject} ORDER BY name DESC LIMIT 1
        """
        )

        connexion.commit()
        logger.debug("Message deleted from buffer")

        cursor.close()
        connexion.close()


Dependable.register(Buffer)
