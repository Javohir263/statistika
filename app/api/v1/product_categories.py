"""ProductCategory CRUD endpointlari."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.product_category import ProductCategory
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)

router = APIRouter(prefix="/product-categories", tags=["Product Categories"])


@router.get("/", response_model=list[ProductCategoryRead])
async def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ProductCategory).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{category_id}", response_model=ProductCategoryRead)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(ProductCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: ProductCategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    category = ProductCategory(**payload.model_dump())
    db.add(category)
    try:
        await db.commit()
        await db.refresh(category)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create: {e}")
    return category


@router.patch("/{category_id}", response_model=ProductCategoryRead)
async def update_category(
    category_id: int,
    payload: ProductCategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    category = await db.get(ProductCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(ProductCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
