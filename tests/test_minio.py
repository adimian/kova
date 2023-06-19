import io

from loguru import logger


def test_minio_can_create_bucket(minio):
    found = minio.bucket_exists("minio-test")
    if not found:
        minio.make_bucket("minio-test")
    else:
        logger.debug("Bucket 'minio-test' already exists")

    found = minio.bucket_exists("minio-test")
    assert found


def test_minio_can_put_object(minio):
    minio.put_object("minio-test", "object-test", io.BytesIO(b"hello"), 5)
    response = minio.get_object("minio-test", "object-test")
    assert response.data == b"hello"
