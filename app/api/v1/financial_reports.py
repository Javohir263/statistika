"""FinancialReport CRUD endpointlari."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.financial_report import FinancialReport
from app.schemas.financial_report import (
    FinancialReportCreate,
    FinancialReportRead,
    FinancialReportUpdate,
)

router = APIRouter(prefix="/financial-reports", tags=["Financial Reports"])


@router.get("/", response_model=list[FinancialReportRead])
async def list_reports(
    company_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Moliyaviy hisobotlar. company_id, year, month bilan filtrlash."""
    query = select(FinancialReport)
    if company_id is not None:
        query = query.where(FinancialReport.company_id == company_id)
    if year is not None:
        query = query.where(FinancialReport.year == year)
    if month is not None:
        query = query.where(FinancialReport.month == month)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{report_id}", response_model=FinancialReportRead)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(FinancialReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/", response_model=FinancialReportRead, status_code=status.HTTP_201_CREATED)
async def create_report(
    payload: FinancialReportCreate,
    db: AsyncSession = Depends(get_db),
):
    report = FinancialReport(**payload.model_dump())
    db.add(report)
    try:
        await db.commit()
        await db.refresh(report)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not create: {e}")
    return report


@router.patch("/{report_id}", response_model=FinancialReportRead)
async def update_report(
    report_id: int,
    payload: FinancialReportUpdate,
    db: AsyncSession = Depends(get_db),
):
    report = await db.get(FinancialReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(report, key, value)

    await db.commit()
    await db.refresh(report)
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(FinancialReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    await db.delete(report)
    await db.commit()
