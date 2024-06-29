from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.api.libs.redis import check_redis_connection
from app.core.database import engine
from app.main import app

client = TestClient(app)


@pytest.fixture()
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio()
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio()
async def test_check_redis_connection():
    connection_status = await check_redis_connection()
    assert connection_status is True


@pytest.mark.asyncio()
async def test_check_database_connection():
    try:
        with engine.connect() as connection:
            assert connection is not None
    except Exception as e:
        pytest.fail(f"Falha ao conectar ao banco de dados: {e}")
