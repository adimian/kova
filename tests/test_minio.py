import io


def test_minio_can_create_bucket(minio):
    minio["client"].make_bucket(minio["bucket"])
    found = minio["client"].bucket_exists(minio["bucket"])
    assert found


def test_minio_can_put_object(minio):
    minio["client"].put_object(
        minio["bucket"], "object-test", io.BytesIO(b"hello"), 5
    )
    response = minio["client"].get_object(minio["bucket"], "object-test")
    assert response.data == b"hello"


def test_can_delete_bucket(minio):
    minio["client"].remove_object(minio["bucket"], "object-test")
    minio["client"].remove_bucket(minio["bucket"])
    found = minio["client"].bucket_exists(minio["bucket"])
    assert not found
