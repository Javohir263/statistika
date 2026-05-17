"""Sector CRUD endpointlari."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.sector import Sector
from app.schemas.sector import SectorCreate, SectorRead, SectorUpdate

router = APIRouter(prefix="/sectors", tags=["Sectors"])


@router.get("/", response_model=list[SectorRead])
async def list_sectors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Barcha sohalarni qaytarish (pagination bilan)."""
    result = await db.execute(select(Sector).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{sector_id}", response_model=SectorRead)
async def get_sector(sector_id: int, db: AsyncSession = Depends(get_db)):
    """Bitta sohani ID bo'yicha qaytarish."""
    sector = await db.get(Sector, sector_id)
    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sector with id={sector_id} not found",
        )
    return sector


@router.post("/", response_model=SectorRead, status_code=status.HTTP_201_CREATED)
async def create_sector(
    payload: SectorCreate,
    db: AsyncSession = Depends(get_db),
):
    """Yangi soha yaratish."""
    sector = Sector(**payload.model_dump())
    db.add(sector)
    try:
        await db.commit()
        await db.refresh(sector)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create sector: {e}",
        )
    return sector


@router.patch("/{sector_id}", response_model=SectorRead)
async def update_sector(
    sector_id: int,
    payload: SectorUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Sohani qisman yangilash."""
    sector = await db.get(Sector, sector_id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sector, key, value)

    await db.commit()
    await db.refresh(sector)
    return sector


@router.delete("/{sector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sector(sector_id: int, db: AsyncSession = Depends(get_db)):
    """Sohani o'chirish (uning kompaniyalari ham CASCADE bilan o'chadi)."""
    sector = await db.get(Sector, sector_id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    await db.delete(sector)
    await db.commit()