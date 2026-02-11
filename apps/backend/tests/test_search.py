import pytest
from httpx import AsyncClient

from app.models import Website


class TestSearch:
    async def test_search_no_query(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/search")
        assert response.status_code == 422

    async def test_search_empty_results(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/search?q=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_search_by_title(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.get("/api/v1/search?q=Example")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(w["slug"] == "example-site" for w in data["items"])

    async def test_search_by_description(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.get("/api/v1/search?q=example+website")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    async def test_search_pagination(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/search?q=Test&page=1&size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["pages"] == 3

    async def test_search_case_insensitive(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.get("/api/v1/search?q=EXAMPLE")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
