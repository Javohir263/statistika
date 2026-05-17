from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyBase(BaseModel):
    """Tarmoq umumiy maydonlari."""
    name: str = Field(..., min_length=2, max_length=150)
    sector_id: int = Field(..., gt=0, description="Sector ID")
    founded_year: int | None = Field(None, ge=1900, le=2100)
    headquarters: str | None = Field(None, max_length=255)
    website: str | None = Field(None, max_length=255)
    description: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    sector_id: int | None = Field(None, gt=0)
    founded_year: int | None = Field(None, ge=1900, le=2100)
    headquarters: str | None = None
    website: str | None = None
    description: str | None = None


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)