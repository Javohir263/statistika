from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Foydalanuvchi umumiy maydonlari."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str | None = Field(None, max_length=150)


class UserCreate(UserBase):
    """Ro'yxatdan o'tish — POST /api/v1/users/register."""
    password: str = Field(..., min_length=8, description="Kamida 8 belgi")


class UserUpdate(BaseModel):
    """Ma'lumotlarni yangilash."""
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    """API javobi — PAROL CHIQARILMAYDI!"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)