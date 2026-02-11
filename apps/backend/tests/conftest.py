from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token, get_password_hash
from app.database import Base, get_db
from app.main import app
from app.models import Category, Collection, Platform, Style, User, Website


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async_session_test = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_test() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def async_empty_generator():
    """Empty async generator for mocking scan_iter."""
    return
    yield  # Make it an async generator


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = override_get_db

    # Mock Redis functions
    with patch("app.core.cache.get_redis", new_callable=AsyncMock) as mock_redis:
        mock_redis_client = AsyncMock()
        mock_redis_client.get = AsyncMock(return_value=None)
        mock_redis_client.set = AsyncMock()
        mock_redis_client.delete = AsyncMock()
        mock_redis_client.scan_iter = lambda **kwargs: async_empty_generator()
        mock_redis_client.close = AsyncMock()
        mock_redis.return_value = mock_redis_client

        with patch("app.core.cache.close_redis", new_callable=AsyncMock):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as ac:
                yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        is_superuser=False,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword123"),
        full_name="Admin User",
        is_superuser=True,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def user_token(test_user: User) -> str:
    return create_access_token(data={"sub": test_user.email})


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(data={"sub": admin_user.email})


@pytest.fixture
def auth_headers(user_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
async def test_category(db_session: AsyncSession) -> Category:
    category = Category(
        slug="minimal",
        title="Minimal",
        description="Clean minimal designs",
        icon="ph:minus",
        website_count=0,
        sort_order=1,
        is_active=True,
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest.fixture
async def test_style(db_session: AsyncSession) -> Style:
    style = Style(
        slug="dark-mode",
        title="Dark Mode",
        website_count=0,
        is_active=True,
    )
    db_session.add(style)
    await db_session.commit()
    await db_session.refresh(style)
    return style


@pytest.fixture
async def test_collection(db_session: AsyncSession) -> Collection:
    collection = Collection(
        slug="gsap-animations",
        title="GSAP Animations",
        description="Websites with GSAP animations",
        website_count=0,
        is_active=True,
    )
    db_session.add(collection)
    await db_session.commit()
    await db_session.refresh(collection)
    return collection


@pytest.fixture
async def test_platform(db_session: AsyncSession) -> Platform:
    platform = Platform(
        slug="webflow",
        title="Webflow",
        website_url="https://webflow.com",
        website_count=0,
        is_active=True,
    )
    db_session.add(platform)
    await db_session.commit()
    await db_session.refresh(platform)
    return platform


@pytest.fixture
async def test_website(
    db_session: AsyncSession,
    test_category: Category,
    test_platform: Platform,
) -> Website:
    website = Website(
        slug="example-site",
        title="Example Site",
        description="An example website",
        original_url="https://example.com",
        thumbnail_url="https://example.com/thumb.jpg",
        image_url="https://example.com/image.jpg",
        platform_id=test_platform.id,
        is_featured=False,
        is_active=True,
        view_count=0,
    )
    website.categories.append(test_category)
    db_session.add(website)
    await db_session.commit()
    await db_session.refresh(website)
    return website


@pytest.fixture
async def test_website_with_style(
    db_session: AsyncSession,
    test_category: Category,
    test_style: Style,
    test_platform: Platform,
) -> Website:
    website = Website(
        slug="styled-site",
        title="Styled Site",
        description="A website with style",
        original_url="https://styled.com",
        thumbnail_url="https://styled.com/thumb.jpg",
        image_url="https://styled.com/image.jpg",
        platform_id=test_platform.id,
        is_featured=False,
        is_active=True,
        view_count=0,
    )
    website.categories.append(test_category)
    website.styles.append(test_style)
    db_session.add(website)
    await db_session.commit()
    await db_session.refresh(website)
    return website


@pytest.fixture
async def test_website_with_collection(
    db_session: AsyncSession,
    test_category: Category,
    test_collection: Collection,
    test_platform: Platform,
) -> Website:
    website = Website(
        slug="collection-site",
        title="Collection Site",
        description="A website in collection",
        original_url="https://collection.com",
        thumbnail_url="https://collection.com/thumb.jpg",
        image_url="https://collection.com/image.jpg",
        platform_id=test_platform.id,
        is_featured=False,
        is_active=True,
        view_count=0,
    )
    website.categories.append(test_category)
    website.collections.append(test_collection)
    db_session.add(website)
    await db_session.commit()
    await db_session.refresh(website)
    return website


@pytest.fixture
async def test_websites(
    db_session: AsyncSession,
    test_category: Category,
    test_platform: Platform,
) -> list[Website]:
    websites = []
    for i in range(5):
        website = Website(
            slug=f"test-site-{i}",
            title=f"Test Site {i}",
            description=f"Description for test site {i}",
            original_url=f"https://test{i}.com",
            thumbnail_url=f"https://test{i}.com/thumb.jpg",
            image_url=f"https://test{i}.com/image.jpg",
            platform_id=test_platform.id,
            is_featured=i < 2,
            is_active=True,
            view_count=i * 10,
        )
        website.categories.append(test_category)
        db_session.add(website)
        websites.append(website)

    await db_session.commit()
    for website in websites:
        await db_session.refresh(website)
    return websites
