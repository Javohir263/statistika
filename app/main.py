"""Statistics Platform API — kirish nuqtasi."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App ishga tushganda va to'xtaganda bajariladi."""
    # Startup
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} ishga tushdi")
    yield
    # Shutdown
    print("🛑 App to'xtatilmoqda...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Restoran, Supermarketlar uchun statistik tahlil platformasi",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — frontend va boshqa domenlardan so'rovlar uchun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routerlarini ulash (/api/v1 prefix bilan)
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Asosiy sahifa — health check."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check — server tirikmi?"""
    return {"status": "healthy"}