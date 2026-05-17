"""Statistik endpointlar — loyihaning asosiy qiymati.

Bu endpointlar SUM, COUNT, GROUP BY kabi aggregate funksiyalarni ishlatadi.
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.branch import Branch
from app.models.company import Company
from app.models.financial_report import FinancialReport
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.sales import Sale
from app.schemas.stats import (
    CategoryShareItem,
    CompanyComparisonItem,
    GrowthItem,
    IncomeMonthlyResponse,
    IncomeYearlyResponse,
    InventoryRemainingItem,
    TopProductItem,
)

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/income/yearly", response_model=list[IncomeYearlyResponse])
async def income_yearly(
    company_id: int | None = None,
    year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Yillik kirim — kompaniya va yil bo'yicha jamlangan."""
    query = (
        select(
            Company.id.label("company_id"),
            Company.name.label("company_name"),
            FinancialReport.year,
            func.sum(FinancialReport.income).label("total_income"),
            func.sum(FinancialReport.expense).label("total_expense"),
            func.sum(FinancialReport.net_profit).label("net_profit"),
        )
        .join(FinancialReport, FinancialReport.company_id == Company.id)
        .group_by(Company.id, Company.name, FinancialReport.year)
        .order_by(Company.name, FinancialReport.year)
    )
    if company_id is not None:
        query = query.where(Company.id == company_id)
    if year is not None:
        query = query.where(FinancialReport.year == year)

    result = await db.execute(query)
    return [
        IncomeYearlyResponse(
            company_id=row.company_id,
            company_name=row.company_name,
            year=row.year,
            total_income=row.total_income or Decimal(0),
            total_expense=row.total_expense or Decimal(0),
            net_profit=row.net_profit or Decimal(0),
        )
        for row in result.all()
    ]


@router.get("/income/monthly", response_model=list[IncomeMonthlyResponse])
async def income_monthly(
    company_id: int | None = None,
    year: int | None = None,
    month: int | None = Query(None, ge=1, le=12),
    db: AsyncSession = Depends(get_db),
):
    """Oylik kirim — har oy uchun alohida."""
    query = (
        select(
            Company.id.label("company_id"),
            Company.name.label("company_name"),
            FinancialReport.year,
            FinancialReport.month,
            FinancialReport.income,
            FinancialReport.expense,
            FinancialReport.net_profit,
        )
        .join(FinancialReport, FinancialReport.company_id == Company.id)
        .order_by(Company.name, FinancialReport.year, FinancialReport.month)
    )
    if company_id is not None:
        query = query.where(Company.id == company_id)
    if year is not None:
        query = query.where(FinancialReport.year == year)
    if month is not None:
        query = query.where(FinancialReport.month == month)

    result = await db.execute(query)
    return [
        IncomeMonthlyResponse(
            company_id=row.company_id,
            company_name=row.company_name,
            year=row.year,
            month=row.month,
            income=row.income,
            expense=row.expense,
            net_profit=row.net_profit,
        )
        for row in result.all()
    ]


@router.get("/top-products", response_model=list[TopProductItem])
async def top_products(
    sector_id: int | None = None,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Eng ko'p sotilgan mahsulotlar."""
    query = (
        select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            ProductCategory.name.label("category_name"),
            func.sum(Sale.quantity).label("total_quantity_sold"),
            func.sum(Sale.total_amount).label("total_revenue"),
        )
        .join(Sale, Sale.product_id == Product.id)
        .join(ProductCategory, Product.category_id == ProductCategory.id)
        .group_by(Product.id, Product.name, ProductCategory.name)
        .order_by(desc("total_revenue"))
        .limit(limit)
    )
    if sector_id is not None:
        query = (
            query.join(Branch, Branch.id == Sale.branch_id)
            .join(Company, Company.id == Branch.company_id)
            .where(Company.sector_id == sector_id)
        )

    result = await db.execute(query)
    return [
        TopProductItem(
            product_id=row.product_id,
            product_name=row.product_name,
            category_name=row.category_name,
            total_quantity_sold=row.total_quantity_sold or Decimal(0),
            total_revenue=row.total_revenue or Decimal(0),
        )
        for row in result.all()
    ]


@router.get("/inventory-remaining", response_model=list[InventoryRemainingItem])
async def inventory_remaining(
    branch_id: int | None = None,
    min_quantity: float = 0,
    db: AsyncSession = Depends(get_db),
):
    """Omborda qolgan mahsulotlar."""
    query = (
        select(
            Branch.id.label("branch_id"),
            Branch.name.label("branch_name"),
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Inventory.quantity,
            Product.unit,
        )
        .join(Branch, Branch.id == Inventory.branch_id)
        .join(Product, Product.id == Inventory.product_id)
        .where(Inventory.quantity >= min_quantity)
        .order_by(Branch.name, Product.name)
    )
    if branch_id is not None:
        query = query.where(Branch.id == branch_id)

    result = await db.execute(query)
    return [
        InventoryRemainingItem(
            branch_id=row.branch_id,
            branch_name=row.branch_name,
            product_id=row.product_id,
            product_name=row.product_name,
            quantity=row.quantity,
            unit=row.unit,
        )
        for row in result.all()
    ]


@router.get("/compare-companies", response_model=list[CompanyComparisonItem])
async def compare_companies(
    sector_id: int | None = None,
    year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Tarmoqlarni taqqoslash — kim ko'p ishlab topgan?"""
    query = (
        select(
            Company.id.label("company_id"),
            Company.name.label("company_name"),
            func.coalesce(func.sum(FinancialReport.income), 0).label("total_income"),
            func.coalesce(func.sum(FinancialReport.expense), 0).label("total_expense"),
            func.coalesce(func.sum(FinancialReport.net_profit), 0).label("net_profit"),
            func.count(func.distinct(Branch.id)).label("branches_count"),
        )
        .outerjoin(FinancialReport, FinancialReport.company_id == Company.id)
        .outerjoin(Branch, Branch.company_id == Company.id)
        .group_by(Company.id, Company.name)
        .order_by(desc("net_profit"))
    )
    if sector_id is not None:
        query = query.where(Company.sector_id == sector_id)
    if year is not None:
        query = query.where(FinancialReport.year == year)

    result = await db.execute(query)
    return [
        CompanyComparisonItem(
            company_id=row.company_id,
            company_name=row.company_name,
            total_income=row.total_income,
            total_expense=row.total_expense,
            net_profit=row.net_profit,
            branches_count=row.branches_count,
        )
        for row in result.all()
    ]


@router.get("/category-share", response_model=list[CategoryShareItem])
async def category_share(
    company_id: int | None = None,
    year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Mahsulot kategoriyalari bo'yicha sotuv ulushi (foizda)."""
    # Avval umumiy sotuvni hisoblaymiz
    total_query = select(func.sum(Sale.total_amount))
    if company_id is not None:
        total_query = total_query.join(Branch, Branch.id == Sale.branch_id).where(
            Branch.company_id == company_id
        )

    total_result = await db.execute(total_query)
    total = total_result.scalar() or Decimal(0)

    if total == 0:
        raise HTTPException(status_code=404, detail="No sales data available")

    # Endi har kategoriya bo'yicha
    cat_query = (
        select(
            ProductCategory.id.label("category_id"),
            ProductCategory.name.label("category_name"),
            func.sum(Sale.total_amount).label("total_sales"),
        )
        .join(Product, Product.category_id == ProductCategory.id)
        .join(Sale, Sale.product_id == Product.id)
        .group_by(ProductCategory.id, ProductCategory.name)
        .order_by(desc("total_sales"))
    )
    if company_id is not None:
        cat_query = cat_query.join(Branch, Branch.id == Sale.branch_id).where(
            Branch.company_id == company_id
        )

    cat_result = await db.execute(cat_query)
    return [
        CategoryShareItem(
            category_id=row.category_id,
            category_name=row.category_name,
            total_sales=row.total_sales,
            share_percentage=float(row.total_sales / total * 100),
        )
        for row in cat_result.all()
    ]


@router.get("/growth", response_model=list[GrowthItem])
async def growth(
    company_id: int = Query(..., gt=0),
    from_year: int = Query(..., ge=1990, le=2100),
    to_year: int = Query(..., ge=1990, le=2100),
    db: AsyncSession = Depends(get_db),
):
    """O'sish dinamikasi — yillar bo'yicha kompaniya foydasi."""
    query = (
        select(
            FinancialReport.year,
            func.sum(FinancialReport.income).label("total_income"),
            func.sum(FinancialReport.net_profit).label("total_profit"),
        )
        .where(
            FinancialReport.company_id == company_id,
            FinancialReport.year >= from_year,
            FinancialReport.year <= to_year,
        )
        .group_by(FinancialReport.year)
        .order_by(FinancialReport.year)
    )

    result = await db.execute(query)
    rows = result.all()

    items: list[GrowthItem] = []
    prev_income: Decimal | None = None
    for row in rows:
        growth_pct = None
        if prev_income is not None and prev_income > 0:
            growth_pct = float((row.total_income - prev_income) / prev_income * 100)
        items.append(
            GrowthItem(
                year=row.year,
                total_income=row.total_income or Decimal(0),
                total_profit=row.total_profit or Decimal(0),
                growth_percentage=growth_pct,
            )
        )
        prev_income = row.total_income

    return items
