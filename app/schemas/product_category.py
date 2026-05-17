from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCategoryBase(BaseModel):
    """Kategoriya umumiy maydonlari."""
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = None


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None


class ProductCategoryRead(ProductCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)