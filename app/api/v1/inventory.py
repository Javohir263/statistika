"""Inventory CRUD endpointlari."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=list[InventoryRead])
async def list_inventory(
    branch_id: int | None = None,
    product_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Ombor ro'yxati. branch_id, product_id orqali filtrlash."""
    query = select(Inventory)
    if branch_id is not None:
        query = query.where(Inventory.branch_id == branch_id)
    if product_id is not None:
        query = query.where(Inventory.product_id == product_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{inventory_id}", response_model=InventoryRead)
async def get_inventory(inventory_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Inventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.post("/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    payload: InventoryCreate,
    db: AsyncSession = Depends(get_db),
):
    item = Inventory(**payload.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create: {e}")
    return item


@router.patch("/{inventory_id}", response_model=InventoryRead)
async def update_inventory(
    inventory_id: int,
    payload: InventoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    item = await db.get(Inventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Inventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    await db.delete(item)
    await db.commit()
