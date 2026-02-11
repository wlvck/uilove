import pytest
from httpx import AsyncClient

from app.models import User


class TestAuthLogin:
    async def test_login_success(self, client: AsyncClient, test_user: User) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpassword123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, test_user: User) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    async def test_login_nonexistent_user(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    async def test_login_inactive_user(
        self, client: AsyncClient, db_session, test_user: User
    ) -> None:
        # Note: Current implementation allows inactive users to login
        # This test documents the current behavior
        test_user.is_active = False
        await db_session.commit()

        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpassword123"},
        )
        # Current behavior: inactive users can still login
        assert response.status_code == 200


class TestAuthMe:
    async def test_get_me_authenticated(
        self, client: AsyncClient, test_user: User, auth_headers: dict[str, str]
    ) -> None:
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert data["is_superuser"] is False

    async def test_get_me_unauthenticated(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient) -> None:
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401

    async def test_get_me_admin(
        self, client: AsyncClient, admin_user: User, admin_headers: dict[str, str]
    ) -> None:
        response = await client.get("/api/v1/auth/me", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@example.com"
        assert data["is_superuser"] is True
