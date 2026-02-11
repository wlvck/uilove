import pytest
from httpx import AsyncClient

from app.models import Category, Platform, Website


class TestWebsitesList:
    async def test_list_websites_empty(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/websites")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1

    async def test_list_websites(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 5
        assert data["total"] == 5

    async def test_list_websites_pagination(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites?page=1&size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["pages"] == 3
        assert data["page"] == 1
        assert data["size"] == 2

    async def test_list_websites_page_2(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites?page=2&size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 2

    async def test_list_websites_filter_by_category(
        self, client: AsyncClient, test_websites: list[Website], test_category: Category
    ) -> None:
        response = await client.get(f"/api/v1/websites?category={test_category.slug}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 5


class TestWebsiteDetail:
    async def test_get_website_by_slug(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.get(f"/api/v1/websites/{test_website.slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == "example-site"
        assert data["title"] == "Example Site"
        assert "categories" in data
        assert "platform" in data

    async def test_get_website_not_found(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/websites/nonexistent-slug")
        assert response.status_code == 404

    async def test_get_website_increments_view_count(
        self, client: AsyncClient, test_website: Website, db_session
    ) -> None:
        initial_count = test_website.view_count

        await client.get(f"/api/v1/websites/{test_website.slug}")
        await db_session.refresh(test_website)

        assert test_website.view_count == initial_count + 1


class TestFeaturedWebsites:
    async def test_get_featured_websites(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites/featured")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        for website in data:
            assert website["is_featured"] is True


class TestLatestWebsites:
    async def test_get_latest_websites(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites/latest")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10


class TestPopularWebsites:
    async def test_get_popular_websites(
        self, client: AsyncClient, test_websites: list[Website]
    ) -> None:
        response = await client.get("/api/v1/websites/popular")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10
        if len(data) > 1:
            assert data[0]["view_count"] >= data[1]["view_count"]


class TestWebsiteCreate:
    async def test_create_website_as_admin(
        self,
        client: AsyncClient,
        admin_headers: dict[str, str],
        test_category: Category,
        test_platform: Platform,
    ) -> None:
        website_data = {
            "slug": "new-website",
            "title": "New Website",
            "description": "A new website description",
            "original_url": "https://newwebsite.com",
            "thumbnail_url": "https://newwebsite.com/thumb.jpg",
            "image_url": "https://newwebsite.com/image.jpg",
            "platform_id": test_platform.id,
            "category_ids": [test_category.id],
            "style_ids": [],
            "collection_ids": [],
            "is_featured": True,
        }
        response = await client.post(
            "/api/v1/websites",
            json=website_data,
            headers=admin_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["slug"] == "new-website"
        assert data["title"] == "New Website"
        assert data["is_featured"] is True

    async def test_create_website_unauthenticated(self, client: AsyncClient) -> None:
        website_data = {
            "slug": "new-website",
            "title": "New Website",
        }
        response = await client.post("/api/v1/websites", json=website_data)
        assert response.status_code == 401

    async def test_create_website_non_admin(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        website_data = {
            "slug": "new-website",
            "title": "New Website",
        }
        response = await client.post(
            "/api/v1/websites",
            json=website_data,
            headers=auth_headers,
        )
        assert response.status_code == 403

    async def test_create_website_duplicate_slug(
        self,
        client: AsyncClient,
        admin_headers: dict[str, str],
        test_website: Website,
    ) -> None:
        website_data = {
            "slug": test_website.slug,
            "title": "Another Website",
        }
        response = await client.post(
            "/api/v1/websites",
            json=website_data,
            headers=admin_headers,
        )
        assert response.status_code == 409


class TestWebsiteUpdate:
    async def test_update_website_as_admin(
        self,
        client: AsyncClient,
        admin_headers: dict[str, str],
        test_website: Website,
    ) -> None:
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
        }
        response = await client.put(
            f"/api/v1/websites/{test_website.slug}",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"

    async def test_update_website_unauthenticated(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.put(
            f"/api/v1/websites/{test_website.slug}",
            json={"title": "New Title"},
        )
        assert response.status_code == 401

    async def test_update_website_non_admin(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        test_website: Website,
    ) -> None:
        response = await client.put(
            f"/api/v1/websites/{test_website.slug}",
            json={"title": "New Title"},
            headers=auth_headers,
        )
        assert response.status_code == 403

    async def test_update_website_not_found(
        self, client: AsyncClient, admin_headers: dict[str, str]
    ) -> None:
        response = await client.put(
            "/api/v1/websites/nonexistent",
            json={"title": "New Title"},
            headers=admin_headers,
        )
        assert response.status_code == 404


class TestWebsiteDelete:
    async def test_delete_website_as_admin(
        self,
        client: AsyncClient,
        admin_headers: dict[str, str],
        test_website: Website,
    ) -> None:
        response = await client.delete(
            f"/api/v1/websites/{test_website.slug}",
            headers=admin_headers,
        )
        assert response.status_code == 204

        response = await client.get(f"/api/v1/websites/{test_website.slug}")
        assert response.status_code == 404

    async def test_delete_website_unauthenticated(
        self, client: AsyncClient, test_website: Website
    ) -> None:
        response = await client.delete(f"/api/v1/websites/{test_website.slug}")
        assert response.status_code == 401

    async def test_delete_website_non_admin(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        test_website: Website,
    ) -> None:
        response = await client.delete(
            f"/api/v1/websites/{test_website.slug}",
            headers=auth_headers,
        )
        assert response.status_code == 403

    async def test_delete_website_not_found(
        self, client: AsyncClient, admin_headers: dict[str, str]
    ) -> None:
        response = await client.delete(
            "/api/v1/websites/nonexistent",
            headers=admin_headers,
        )
        assert response.status_code == 404
