"""Admin endpointlari — faqat SECRET_KEY bilan kirish mumkin."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.services.seed import seed_all

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed", status_code=status.HTTP_200_OK)
async def trigger_seed(
    secret: str = Query(..., description="SECRET_KEY ni kiriting"),
    days_of_sales: int = Query(30, ge=1, le=180, description="Necha kunlik sotuvlar"),
    db: AsyncSession = Depends(get_db),
):
    """Bazaga test ma'lumotlarini yuklash.

    Bu endpoint SECRET_KEY bilan himoyalangan.
    Production'da bir marta ishlatish uchun mo'ljallangan.
    """
    if secret != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid secret key",
        )

    try:
        result = await seed_all(db, days_of_sales=days_of_sales)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Seed failed: {e}",
        )

    return {
        "status": "success",
        "message": "Ma'lumotlar muvaffaqiyatli yuklandi",
        "data": result,
    }
