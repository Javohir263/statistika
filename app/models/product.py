from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.inventory import Inventory
    from app.models.product_category import ProductCategory
    from app.models.sales import Sale


class Product(Base, TimestampMixin):
    """Mahsulot jadvali — Coca-Cola, Mol go'shti, Olma, Pishloq..."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(20), nullable=False, default="dona")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Bog'lanishlar
    category: Mapped["ProductCategory"] = relationship(back_populates="products")
    inventory_items: Mapped[list["Inventory"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
    sales: Mapped[list["Sale"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name!r}, price={self.price})>"