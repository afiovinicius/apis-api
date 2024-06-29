from http import HTTPStatus

from fastapi.testclient import TestClient

from app.api.libs.redis import check_redis_connection
from app.core.database import engine
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_check_redis_connection():
    connection_status = check_redis_connection()
    assert connection_status is not None


def test_check_database_connection():
    with engine.connect() as connection:
        assert connection is not None
