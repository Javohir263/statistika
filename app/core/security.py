"""Xavfsizlik yordamchi funksiyalari.

Parol hashing: SHA256 (eski foydalanuvchilar bilan moslik uchun)
Token: JWT (python-jose)
"""
import hashlib
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


# ─── PAROL HASHING (SHA256 — eski kod bilan moslik) ──────
def get_password_hash(password: str) -> str:
    """Parolni SHA256 hash qiladi."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni tekshirish."""
    return get_password_hash(plain_password) == hashed_password


# ─── JWT TOKEN ───────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWT access token yaratadi.
    
    Args:
        data: Token ichiga yoziladigan ma'lumot (masalan: {"sub": user_id})
        expires_delta: Token qancha vaqt amal qiladi (default: .env'dan)
    
    Returns:
        Imzolangan JWT token (string)
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """JWT tokenni ochib, ichidagi ma'lumotni qaytaradi.
    
    Args:
        token: JWT token string
    
    Returns:
        Token ichidagi ma'lumot (dict) yoki None (agar xato bo'lsa)
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None