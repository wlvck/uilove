import pytest
from httpx import AsyncClient

from app.models import Platform


class TestPlatformsList:
    async def test_list_platforms_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/platforms")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    async def test_list_platforms(
        self, client: AsyncClient, test_platform: Platform
    ) -> None:
        response = await client.get("/api/v1/platforms")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["slug"] == "webflow"
        assert data[0]["title"] == "Webflow"
