from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class BranchBase(BaseModel):
    """Filial umumiy maydonlari."""
    company_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=200)
    city: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=500)
    opening_date: date | None = None


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    company_id: int | None = Field(None, gt=0)
    name: str | None = Field(None, min_length=2, max_length=200)
    city: str | None = Field(None, min_length=2, max_length=100)
    address: str | None = Field(None, min_length=5, max_length=500)
    opening_date: date | None = None


class BranchRead(BranchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)