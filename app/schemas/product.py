from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Mahsulot umumiy maydonlari."""
    category_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=200)
    price: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    unit: str = Field(default="dona", max_length=20)
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = Field(None, gt=0)
    name: str | None = Field(None, min_length=2, max_length=200)
    price: Decimal | None = Field(None, ge=0, max_digits=12, decimal_places=2)
    unit: str | None = Field(None, max_length=20)
    description: str | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)