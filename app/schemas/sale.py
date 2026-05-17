from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    """Sotuv umumiy maydonlari."""
    branch_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0, max_digits=14, decimal_places=3)
    total_amount: Decimal = Field(..., ge=0, max_digits=18, decimal_places=2)
    sale_date: date


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    """Sotuvni odatda yangilanmaydi, lekin tuzatish mumkin."""
    quantity: Decimal | None = Field(None, gt=0, max_digits=14, decimal_places=3)
    total_amount: Decimal | None = Field(None, ge=0, max_digits=18, decimal_places=2)
    sale_date: date | None = None


class SaleRead(SaleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)