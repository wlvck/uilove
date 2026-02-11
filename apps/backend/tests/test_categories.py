import pytest
from httpx import AsyncClient

from app.models import Category, Website


class TestCategoriesList:
    async def test_list_categories_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    async def test_list_categories(
        self, client: AsyncClient, test_category: Category
    ) -> None:
        response = await client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["slug"] == "minimal"
        assert data[0]["title"] == "Minimal"
        assert "website_count" in data[0]


class TestCategoryWebsites:
    async def test_get_websites_by_category(
        self, client: AsyncClient, test_category: Category, test_website: Website
    ) -> None:
        response = await client.get(f"/api/v1/categories/{test_category.slug}/websites")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] >= 1

    async def test_get_websites_by_category_not_found(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/categories/nonexistent/websites")
        assert response.status_code == 404

    async def test_get_websites_by_category_pagination(
        self, client: AsyncClient, test_category: Category, test_websites: list[Website]
    ) -> None:
        response = await client.get(
            f"/api/v1/categories/{test_category.slug}/websites?page=1&size=2"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["pages"] == 3
