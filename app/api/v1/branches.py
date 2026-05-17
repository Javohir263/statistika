"""Branch CRUD endpointlari."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_model=list[BranchRead])
async def list_branches(
    company_id: int | None = None,
    city: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Filiallar ro'yxati. company_id, city orqali filtrlash mumkin."""
    query = select(Branch)
    if company_id is not None:
        query = query.where(Branch.company_id == company_id)
    if city is not None:
        query = query.where(Branch.city.ilike(f"%{city}%"))
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{branch_id}", response_model=BranchRead)
async def get_branch(branch_id: int, db: AsyncSession = Depends(get_db)):
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


@router.post("/", response_model=BranchRead, status_code=status.HTTP_201_CREATED)
async def create_branch(
    payload: BranchCreate,
    db: AsyncSession = Depends(get_db),
):
    branch = Branch(**payload.model_dump())
    db.add(branch)
    try:
        await db.commit()
        await db.refresh(branch)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create: {e}")
    return branch


@router.patch("/{branch_id}", response_model=BranchRead)
async def update_branch(
    branch_id: int,
    payload: BranchUpdate,
    db: AsyncSession = Depends(get_db),
):
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(branch, key, value)

    await db.commit()
    await db.refresh(branch)
    return branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(branch_id: int, db: AsyncSession = Depends(get_db)):
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    await db.delete(branch)
    await db.commit()
