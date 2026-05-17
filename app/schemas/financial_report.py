from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FinancialReportBase(BaseModel):
    """Moliyaviy hisobot umumiy maydonlari."""
    company_id: int = Field(..., gt=0)
    year: int = Field(..., ge=1990, le=2100)
    month: int = Field(..., ge=1, le=12)
    income: Decimal = Field(..., ge=0, max_digits=18, decimal_places=2)
    expense: Decimal = Field(..., ge=0, max_digits=18, decimal_places=2)
    net_profit: Decimal = Field(..., max_digits=18, decimal_places=2)


class FinancialReportCreate(FinancialReportBase):
    pass


class FinancialReportUpdate(BaseModel):
    income: Decimal | None = Field(None, ge=0, max_digits=18, decimal_places=2)
    expense: Decimal | None = Field(None, ge=0, max_digits=18, decimal_places=2)
    net_profit: Decimal | None = Field(None, max_digits=18, decimal_places=2)


class FinancialReportRead(FinancialReportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)