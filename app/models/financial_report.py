from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.company import Company


class FinancialReport(Base, TimestampMixin):
    """Moliyaviy hisobot — kompaniyaning yillik/oylik kirim-chiqim."""

    __tablename__ = "financial_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    income: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    expense: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    net_profit: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)

    # Bog'lanish
    company: Mapped["Company"] = relationship(back_populates="financial_reports")

    # Cheklovlar
    __table_args__ = (
        UniqueConstraint("company_id", "year", "month", name="uq_company_year_month"),
        CheckConstraint("month >= 1 AND month <= 12", name="ck_month_range"),
        CheckConstraint("year >= 1990 AND year <= 2100", name="ck_year_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<FinancialReport(company_id={self.company_id}, "
            f"{self.year}-{self.month:02d}, profit={self.net_profit})>"
        )