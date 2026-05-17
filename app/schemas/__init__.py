"""Pydantic schemalari — API uchun input/output shabloni."""

from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.schemas.financial_report import (
    FinancialReportCreate,
    FinancialReportRead,
    FinancialReportUpdate,
)
from app.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
)
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate
from app.schemas.sector import SectorCreate, SectorRead, SectorUpdate
from app.schemas.stats import (
    CategoryShareItem,
    CompanyComparisonItem,
    GrowthItem,
    IncomeMonthlyResponse,
    IncomeYearlyResponse,
    InventoryRemainingItem,
    TopProductItem,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "BranchCreate", "BranchRead", "BranchUpdate",
    "CompanyCreate", "CompanyRead", "CompanyUpdate",
    "FinancialReportCreate", "FinancialReportRead", "FinancialReportUpdate",
    "InventoryCreate", "InventoryRead", "InventoryUpdate",
    "ProductCategoryCreate", "ProductCategoryRead", "ProductCategoryUpdate",
    "ProductCreate", "ProductRead", "ProductUpdate",
    "SaleCreate", "SaleRead", "SaleUpdate",
    "SectorCreate", "SectorRead", "SectorUpdate",
    "UserCreate", "UserRead", "UserUpdate",
    "CategoryShareItem", "CompanyComparisonItem", "GrowthItem",
    "IncomeMonthlyResponse", "IncomeYearlyResponse",
    "InventoryRemainingItem", "TopProductItem",
]