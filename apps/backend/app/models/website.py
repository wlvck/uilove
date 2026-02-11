from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

website_categories = Table(
    "website_categories",
    Base.metadata,
    Column("website_id", Integer, ForeignKey("websites.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

website_styles = Table(
    "website_styles",
    Base.metadata,
    Column("website_id", Integer, ForeignKey("websites.id", ondelete="CASCADE"), primary_key=True),
    Column("style_id", Integer, ForeignKey("styles.id", ondelete="CASCADE"), primary_key=True),
)

website_collections = Table(
    "website_collections",
    Base.metadata,
    Column("website_id", Integer, ForeignKey("websites.id", ondelete="CASCADE"), primary_key=True),
    Column("collection_id", Integer, ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True),
)


class Website(Base):
    __tablename__ = "websites"
    __table_args__ = (
        Index("ix_websites_fulltext", "title", "description", postgresql_using="gin",
              postgresql_ops={"title": "gin_trgm_ops", "description": "gin_trgm_ops"}),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    original_url: Mapped[str | None] = mapped_column(String(2000))
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(Text)
    platform_id: Mapped[int | None] = mapped_column(ForeignKey("platforms.id"))
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    platform: Mapped["Platform | None"] = relationship(back_populates="websites")  # noqa: F821
    categories: Mapped[list["Category"]] = relationship(  # noqa: F821
        secondary=website_categories, back_populates="websites"
    )
    styles: Mapped[list["Style"]] = relationship(  # noqa: F821
        secondary=website_styles, back_populates="websites"
    )
    collections: Mapped[list["Collection"]] = relationship(  # noqa: F821
        secondary=website_collections, back_populates="websites"
    )
