import pytest
from httpx import AsyncClient

from app.models import Style, Website


class TestStylesList:
    async def test_list_styles_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/styles")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    async def test_list_styles(self, client: AsyncClient, test_style: Style) -> None:
        response = await client.get("/api/v1/styles")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["slug"] == "dark-mode"
        assert data[0]["title"] == "Dark Mode"


class TestStyleWebsites:
    async def test_get_websites_by_style(
        self,
        client: AsyncClient,
        test_style: Style,
        test_website_with_style: Website,
    ) -> None:
        response = await client.get(f"/api/v1/styles/{test_style.slug}/websites")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] == 1

    async def test_get_websites_by_style_not_found(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/styles/nonexistent/websites")
        assert response.status_code == 404

    async def test_get_websites_by_style_empty(
        self, client: AsyncClient, test_style: Style
    ) -> None:
        response = await client.get(f"/api/v1/styles/{test_style.slug}/websites")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
