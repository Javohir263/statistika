from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.inventory import Inventory
    from app.models.sales import Sale


class Branch(Base, TimestampMixin):
    """Filial jadvali — har bir kompaniyaning shahobchasi."""

    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    opening_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Bog'lanishlar
    company: Mapped["Company"] = relationship(back_populates="branches")
    inventory_items: Mapped[list["Inventory"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
    )
    sales: Mapped[list["Sale"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name={self.name!r}, city={self.city!r})>"