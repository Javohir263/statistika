"""API v1 routerlari.

Bu yerda barcha v1 endpointlar birlashtiriladi va asosiy
api_router orqali main.py'ga uzatiladi.
"""
from fastapi import APIRouter

from app.api.v1 import (
    admin,
    branches,
    companies,
    financial_reports,
    inventory,
    product_categories,
    products,
    sales,
    sectors,
    stats,
    users,
)

api_router = APIRouter()


# CRUD routerlari
api_router.include_router(sectors.router)
api_router.include_router(product_categories.router)
api_router.include_router(companies.router)
api_router.include_router(branches.router)
api_router.include_router(products.router)
api_router.include_router(inventory.router)
api_router.include_router(sales.router)
api_router.include_router(financial_reports.router)
api_router.include_router(users.router)

# Statistik endpointlar
api_router.include_router(stats.router)

# Admin endpointlar (seed va boshqalar)
api_router.include_router(admin.router)