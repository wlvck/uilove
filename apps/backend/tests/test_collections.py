import pytest
from httpx import AsyncClient

from app.models import Collection, Website


class TestCollectionsList:
    async def test_list_collections_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/collections")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    async def test_list_collections(
        self, client: AsyncClient, test_collection: Collection
    ) -> None:
        response = await client.get("/api/v1/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["slug"] == "gsap-animations"
        assert data[0]["title"] == "GSAP Animations"
        assert "description" in data[0]


class TestCollectionWebsites:
    async def test_get_websites_by_collection(
        self,
        client: AsyncClient,
        test_collection: Collection,
        test_website_with_collection: Website,
    ) -> None:
        response = await client.get(
            f"/api/v1/collections/{test_collection.slug}/websites"
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] == 1

    async def test_get_websites_by_collection_not_found(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/collections/nonexistent/websites")
        assert response.status_code == 404

    async def test_get_websites_by_collection_empty(
        self, client: AsyncClient, test_collection: Collection
    ) -> None:
        response = await client.get(
            f"/api/v1/collections/{test_collection.slug}/websites"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
