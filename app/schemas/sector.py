from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SectorBase(BaseModel):
    """Sector uchun umumiy maydonlar (DRY tamoyili)."""
    name: str = Field(..., min_length=2, max_length=100, description="Soha nomi")
    description: str | None = Field(None, description="Qisqa izoh")


class SectorCreate(SectorBase):
    """Yangi soha yaratish — POST /api/v1/sectors."""
    pass


class SectorUpdate(BaseModel):
    """Sohani yangilash — PATCH /api/v1/sectors/{id}.
    Barcha maydonlar ixtiyoriy."""
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None


class SectorRead(SectorBase):
    """API javobi — GET /api/v1/sectors/{id}.
    id va vaqtlar bilan."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)