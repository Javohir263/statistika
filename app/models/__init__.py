"""Barcha SQLAlchemy modellari shu yerda import qilinadi.

Alembic va boshqa qismlar modellarni bu yerdan topadi.
Yangi model qo'shilganda — shu yerga qo'shilishi shart.
"""

from app.models.branch import Branch
from app.models.company import Company
from app.models.financial_report import FinancialReport
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.sales import Sale
from app.models.sector import Sector
from app.models.user import User

__all__ = [
    "Branch",
    "Company",
    "FinancialReport",
    "Inventory",
    "Product",
    "ProductCategory",
    "Sale",
    "Sector",
    "User",
]