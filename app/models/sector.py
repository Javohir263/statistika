from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.company import Company


class Sector(Base, TimestampMixin):
    """Soha jadvali — Restoran, Supermarket va h.k."""

    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    companies: Mapped[list["Company"]] = relationship(
        back_populates="sector",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Sector(id={self.id}, name={self.name!r})>"