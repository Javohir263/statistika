from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.branch import Branch
    from app.models.product import Product


class Sale(Base, TimestampMixin):
    """Sotuv jadvali — kunlik/oylik sotuvlar."""

    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Bog'lanishlar
    branch: Mapped["Branch"] = relationship(back_populates="sales")
    product: Mapped["Product"] = relationship(back_populates="sales")

    # Cheklovlar
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_sale_quantity_positive"),
        CheckConstraint("total_amount >= 0", name="ck_total_amount_positive"),
    )

    def __repr__(self) -> str:
        return (
            f"<Sale(branch_id={self.branch_id}, product_id={self.product_id}, "
            f"qty={self.quantity}, total={self.total_amount}, date={self.sale_date})>"
        )