"""Statistik endpointlar uchun response schemalar.

Bu schemalar CRUD'dan farqli — faqat o'qish uchun.
"""
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class IncomeYearlyResponse(BaseModel):
    """Yillik kirim — GET /api/v1/stats/income/yearly."""

    company_id: int
    company_name: str
    year: int
    total_income: Decimal
    total_expense: Decimal
    net_profit: Decimal


class IncomeMonthlyResponse(BaseModel):
    """Oylik kirim — GET /api/v1/stats/income/monthly."""

    company_id: int
    company_name: str
    year: int
    month: int
    income: Decimal
    expense: Decimal
    net_profit: Decimal


class TopProductItem(BaseModel):
    """Top mahsulot — GET /api/v1/stats/top-products."""

    product_id: int
    product_name: str
    category_name: str | None = None
    total_quantity_sold: Decimal
    total_revenue: Decimal


class InventoryRemainingItem(BaseModel):
    """Omborda qolgan — GET /api/v1/stats/inventory-remaining."""

    branch_id: int
    branch_name: str
    product_id: int
    product_name: str
    quantity: Decimal
    unit: str


class CompanyComparisonItem(BaseModel):
    """Tarmoqlar taqqoslash — GET /api/v1/stats/compare-companies."""

    company_id: int
    company_name: str
    total_income: Decimal
    total_expense: Decimal
    net_profit: Decimal
    branches_count: int


class CategoryShareItem(BaseModel):
    """Kategoriya ulushi — GET /api/v1/stats/category-share."""

    category_id: int
    category_name: str
    total_sales: Decimal
    share_percentage: float = Field(..., ge=0, le=100)


class GrowthItem(BaseModel):
    """O'sish dinamikasi — GET /api/v1/stats/growth."""

    year: int
    total_income: Decimal
    total_profit: Decimal
    growth_percentage: float | None = None

    model_config = ConfigDict(from_attributes=True)
