"""Sale CRUD endpointlari."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.sales import Sale
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=list[SaleRead])
async def list_sales(
    branch_id: int | None = None,
    product_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Sotuvlar ro'yxati. branch, product, sana intervali bilan filtrlash."""
    query = select(Sale)
    if branch_id is not None:
        query = query.where(Sale.branch_id == branch_id)
    if product_id is not None:
        query = query.where(Sale.product_id == product_id)
    if date_from is not None:
        query = query.where(Sale.sale_date >= date_from)
    if date_to is not None:
        query = query.where(Sale.sale_date <= date_to)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{sale_id}", response_model=SaleRead)
async def get_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    sale = await db.get(Sale, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
async def create_sale(
    payload: SaleCreate,
    db: AsyncSession = Depends(get_db),
):
    sale = Sale(**payload.model_dump())
    db.add(sale)
    try:
        await db.commit()
        await db.refresh(sale)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create: {e}")
    return sale


@router.patch("/{sale_id}", response_model=SaleRead)
async def update_sale(
    sale_id: int,
    payload: SaleUpdate,
    db: AsyncSession = Depends(get_db),
):
    sale = await db.get(Sale, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(sale, key, value)

    await db.commit()
    await db.refresh(sale)
    return sale


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    sale = await db.get(Sale, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    await db.delete(sale)
    await db.commit()
