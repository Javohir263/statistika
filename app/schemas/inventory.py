from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    """Ombor zapisi umumiy maydonlari."""
    branch_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., ge=0, max_digits=14, decimal_places=3)


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    """Faqat miqdorni yangilash mumkin."""
    quantity: Decimal | None = Field(None, ge=0, max_digits=14, decimal_places=3)


class InventoryRead(InventoryBase):
    id: int
    last_updated: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)