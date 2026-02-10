"""Import data from CSV/JSON files into the database."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.security import get_password_hash
from app.database import Base, async_session, engine
from app.models import Category, User, Website
from app.models.website import website_categories

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


async def import_categories(db: AsyncSession) -> dict[str, int]:
    """Import categories from JSON and return slug->id mapping."""
    path = DATA_DIR / "categories.json"
    if not path.exists():
        print(f"  Skipping: {path} not found")
        return {}

    with open(path) as f:
        data = json.load(f)

    slug_to_id: dict[str, int] = {}
    for i, item in enumerate(data):
        existing = (await db.execute(
            select(Category).where(Category.slug == item["slug"])
        )).scalar_one_or_none()
        if existing:
            slug_to_id[existing.slug] = existing.id
            continue

        cat = Category(
            title=item["title"],
            slug=item["slug"],
            website_count=item.get("count", 0),
            sort_order=i,
        )
        db.add(cat)
        await db.flush()
        slug_to_id[cat.slug] = cat.id

    await db.commit()
    print(f"  Imported {len(slug_to_id)} categories")
    return slug_to_id


async def import_websites(
    db: AsyncSession, category_map: dict[str, int]
) -> None:
    """Import websites from CSV."""
    path = DATA_DIR / "websites_complete.csv"
    if not path.exists():
        print(f"  Skipping: {path} not found")
        return

    df = pd.read_csv(path)
    imported = 0
    skipped = 0

    for _, row in df.iterrows():
        slug = str(row.get("slug", "")).strip()
        if not slug:
            skipped += 1
            continue

        existing = (await db.execute(
            select(Website).where(Website.slug == slug)
        )).scalar_one_or_none()
        if existing:
            skipped += 1
            continue

        website = Website(
            title=str(row.get("title", "")).strip(),
            slug=slug,
            description=str(row.get("description", "")).strip() if pd.notna(row.get("description")) else None,
            original_url=str(row.get("original_url", "")).strip() if pd.notna(row.get("original_url")) else None,
            thumbnail_url=str(row.get("thumbnail", "")).strip() if pd.notna(row.get("thumbnail")) else None,
            image_url=str(row.get("image_url", "")).strip() if pd.notna(row.get("image_url")) else None,
        )
        db.add(website)
        await db.flush()

        # Link categories via junction table directly
        cats_str = str(row.get("categories", ""))
        if pd.notna(row.get("categories")) and cats_str.strip():
            cat_slugs = [s.strip() for s in cats_str.split(",") if s.strip()]
            cat_ids = [category_map[s] for s in cat_slugs if s in category_map]
            if cat_ids:
                await db.execute(
                    insert(website_categories),
                    [{"website_id": website.id, "category_id": cid} for cid in cat_ids],
                )

        imported += 1
        if imported % 100 == 0:
            print(f"  ... {imported} websites imported")
            await db.commit()

    await db.commit()
    print(f"  Imported {imported} websites ({skipped} skipped)")

    # Update category website_count
    from sqlalchemy import func

    for slug, cat_id in category_map.items():
        cat = await db.get(Category, cat_id)
        if cat:
            count = (await db.execute(
                select(func.count()).where(website_categories.c.category_id == cat_id)
            )).scalar_one()
            cat.website_count = count
    await db.commit()
    print("  Updated category counts")


async def create_admin(db: AsyncSession) -> None:
    """Create admin user if it doesn't exist."""
    existing = (await db.execute(
        select(User).where(User.email == settings.admin_email)
    )).scalar_one_or_none()
    if existing:
        print(f"  Admin user already exists: {settings.admin_email}")
        return

    admin = User(
        email=settings.admin_email,
        hashed_password=get_password_hash(settings.admin_password),
        full_name="Admin",
        is_superuser=True,
    )
    db.add(admin)
    await db.commit()
    print(f"  Created admin user: {settings.admin_email}")


async def main(
    import_all: bool = False,
    categories: bool = False,
    websites: bool = False,
    admin: bool = False,
) -> None:
    if import_all:
        categories = websites = admin = True

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        if admin:
            print("Creating admin user...")
            await create_admin(db)

        category_map: dict[str, int] = {}
        if categories or websites:
            print("Importing categories...")
            category_map = await import_categories(db)

        if websites:
            print("Importing websites...")
            await import_websites(db, category_map)

    await engine.dispose()
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import data into UILove database")
    parser.add_argument("--all", action="store_true", help="Import everything")
    parser.add_argument("--categories", action="store_true", help="Import categories")
    parser.add_argument("--websites", action="store_true", help="Import websites")
    parser.add_argument("--admin", action="store_true", help="Create admin user")
    args = parser.parse_args()

    if not any([args.all, args.categories, args.websites, args.admin]):
        parser.print_help()
        sys.exit(1)

    asyncio.run(main(
        import_all=args.all,
        categories=args.categories,
        websites=args.websites,
        admin=args.admin,
    ))
