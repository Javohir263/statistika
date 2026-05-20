"""Autentifikatsiya endpointlari — login va token olish."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2 scheme — Swagger'da "Authorize" tugmasini ishlatish uchun
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ─── DEPENDENCY: Joriy foydalanuvchini olish ──────────────
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """JWT tokenni tekshirib, foydalanuvchini qaytaradi.
    
    Bu funksiya himoyalangan endpoint'larda ishlatiladi:
        async def my_endpoint(current_user: User = Depends(get_current_user)):
            ...
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token noto'g'ri yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Tokenni ochish
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Token ichidan user_id olish
    user_id_str: str | None = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception
    
    # Database'dan foydalanuvchini topish
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas",
        )
    
    return user


# ─── ENDPOINT: Login ──────────────────────────────────────
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Foydalanuvchi login qiladi va JWT token oladi.
    
    Username sifatida email yoki username ishlatish mumkin.
    """
    # Email yoki username bo'yicha foydalanuvchini topish
    result = await db.execute(
        select(User).where(
            (User.email == form_data.username) | (User.username == form_data.username)
        )
    )
    user = result.scalar_one_or_none()
    
    # Foydalanuvchi mavjud emas
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Parol noto'g'ri
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Foydalanuvchi faol emas
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas",
        )
    
    # Token yaratish
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
        },
    }


# ─── ENDPOINT: Joriy foydalanuvchi ma'lumotlari ───────────
@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    """Joriy foydalanuvchi (token egasi) ma'lumotlarini qaytaradi.
    
    Frontend bu endpoint orqali "men kim?" deb so'raydi.
    """
    return current_user