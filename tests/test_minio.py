import io

from minio import Minio
from loguru import logger

from kova.settings import get_settings


def test_minio_can_create_bucket():

    settings = get_settings()
    client = Minio(
        settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )

    found = client.bucket_exists("minio-test")
    if not found:
        client.make_bucket("minio-test")
    else:
        logger.debug("Bucket 'minio-test' already exists")

    found = client.bucket_exists("minio-test")
    assert found


def test_minio_can_put_object():
    settings = get_settings()
    client = Minio(
        settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )
    found = client.bucket_exists("minio-test")
    if not found:
        client.make_bucket("minio-test")
    else:
        logger.debug("Bucket 'minio-test' already exists")
    client.put_object("minio-test", "object-test", io.BytesIO(b"hello"), 5)
    response = client.get_object("minio-test", "object-test")
    assert response.data == b"hello"
