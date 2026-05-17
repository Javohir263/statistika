"""Xavfsizlik yordamchi funksiyalari.

Eslatma: production uchun bcrypt yoki argon2 ishlatish tavsiya etiladi.
Bu yerda imtihon uchun SHA256 bilan oddiy yondashuv.
"""
import hashlib


def get_password_hash(password: str) -> str:
    """Parolni SHA256 hash qiladi."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni tekshirish."""
    return get_password_hash(plain_password) == hashed_password
