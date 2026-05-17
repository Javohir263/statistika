"""Bazaga test ma'lumotlarini yuklash.

Ishlatish:
    python scripts/seed_data.py
"""
import asyncio
import random
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

# Loyiha root'ini Python path'ga qo'shamiz
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

from app.db.session import AsyncSessionLocal, engine  # noqa: E402
from app.models import (  # noqa: E402
    Branch,
    Company,
    FinancialReport,
    Inventory,
    Product,
    ProductCategory,
    Sale,
    Sector,
)


SECTORS = [
    {"name": "Restoran", "description": "Oziq-ovqat tarmog'i — ovqat, pishirish"},
    {"name": "Supermarket", "description": "Yirik do'konlar — keng assortiment"},
]

CATEGORIES = [
    {"name": "Ichimliklar", "description": "Suv, sok, gazli ichimliklar"},
    {"name": "Go'sht mahsulotlari", "description": "Mol, qo'y, tovuq go'shti"},
    {"name": "Sut mahsulotlari", "description": "Sut, qatiq, pishloq, yog'"},
    {"name": "Meva-sabzavot", "description": "Olma, pomidor, sabzi va h.k."},
    {"name": "Non mahsulotlari", "description": "Non, lavash, pirog"},
    {"name": "Shirinliklar", "description": "Konfet, shokolad, pechene"},
    {"name": "Fast-food", "description": "Burger, pizza, lavash"},
    {"name": "Salatlar", "description": "Tayyor salatlar"},
]

COMPANIES = [
    {"name": "Evos", "sector": "Restoran", "founded_year": 2008, "headquarters": "Toshkent", "website": "https://evos.uz"},
    {"name": "Max Way", "sector": "Restoran", "founded_year": 2014, "headquarters": "Toshkent", "website": "https://maxway.uz"},
    {"name": "Bellissimo Pizza", "sector": "Restoran", "founded_year": 2015, "headquarters": "Toshkent", "website": "https://bellissimo.uz"},
    {"name": "Rayhon", "sector": "Restoran", "founded_year": 2010, "headquarters": "Toshkent"},
    {"name": "Sette Bello", "sector": "Restoran", "founded_year": 2016, "headquarters": "Toshkent"},
    {"name": "Korzinka", "sector": "Supermarket", "founded_year": 1998, "headquarters": "Toshkent", "website": "https://korzinka.uz"},
    {"name": "Havas", "sector": "Supermarket", "founded_year": 2010, "headquarters": "Toshkent", "website": "https://havas.uz"},
    {"name": "Olma", "sector": "Supermarket", "founded_year": 2012, "headquarters": "Toshkent"},
    {"name": "Makro", "sector": "Supermarket", "founded_year": 2015, "headquarters": "Toshkent", "website": "https://makro.uz"},
    {"name": "Carrefour", "sector": "Supermarket", "founded_year": 2019, "headquarters": "Toshkent"},
]

PRODUCTS = [
    {"name": "Coca-Cola 1L", "category": "Ichimliklar", "price": Decimal("12000.00"), "unit": "dona"},
    {"name": "Pepsi 1.5L", "category": "Ichimliklar", "price": Decimal("14000.00"), "unit": "dona"},
    {"name": "Suv 1L (Hayot)", "category": "Ichimliklar", "price": Decimal("4000.00"), "unit": "dona"},
    {"name": "Apelsin sharbati", "category": "Ichimliklar", "price": Decimal("18000.00"), "unit": "dona"},
    {"name": "Mol go'shti", "category": "Go'sht mahsulotlari", "price": Decimal("95000.00"), "unit": "kg"},
    {"name": "Qo'y go'shti", "category": "Go'sht mahsulotlari", "price": Decimal("110000.00"), "unit": "kg"},
    {"name": "Tovuq filesi", "category": "Go'sht mahsulotlari", "price": Decimal("55000.00"), "unit": "kg"},
    {"name": "Sut 2.5% 1L", "category": "Sut mahsulotlari", "price": Decimal("13000.00"), "unit": "litr"},
    {"name": "Qatiq 500g", "category": "Sut mahsulotlari", "price": Decimal("8000.00"), "unit": "dona"},
    {"name": "Pishloq 200g", "category": "Sut mahsulotlari", "price": Decimal("25000.00"), "unit": "dona"},
    {"name": "Olma", "category": "Meva-sabzavot", "price": Decimal("18000.00"), "unit": "kg"},
    {"name": "Pomidor", "category": "Meva-sabzavot", "price": Decimal("15000.00"), "unit": "kg"},
    {"name": "Sabzi", "category": "Meva-sabzavot", "price": Decimal("8000.00"), "unit": "kg"},
    {"name": "Non (oddiy)", "category": "Non mahsulotlari", "price": Decimal("3500.00"), "unit": "dona"},
    {"name": "Lavash", "category": "Non mahsulotlari", "price": Decimal("5000.00"), "unit": "dona"},
    {"name": "Snickers", "category": "Shirinliklar", "price": Decimal("9000.00"), "unit": "dona"},
    {"name": "Pechene 200g", "category": "Shirinliklar", "price": Decimal("12000.00"), "unit": "dona"},
    {"name": "Burger", "category": "Fast-food", "price": Decimal("35000.00"), "unit": "dona"},
    {"name": "Pizza Margarita", "category": "Fast-food", "price": Decimal("85000.00"), "unit": "dona"},
    {"name": "Sezar salati", "category": "Salatlar", "price": Decimal("32000.00"), "unit": "dona"},
]

CITIES = ["Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg'ona", "Namangan"]
STREETS = [
    "Amir Temur ko'chasi", "Buyuk Ipak Yo'li", "Bunyodkor ko'chasi",
    "Sayilgoh ko'chasi", "Mustaqillik ko'chasi", "Navoiy ko'chasi",
]


async def seed_sectors(db: AsyncSession) -> dict[str, int]:
    print("Sohalar qo'shilmoqda...")
    sector_map = {}
    for data in SECTORS:
        existing = await db.execute(select(Sector).where(Sector.name == data["name"]))
        sector = existing.scalar_one_or_none()
        if not sector:
            sector = Sector(**data)
            db.add(sector)
            await db.flush()
        sector_map[data["name"]] = sector.id
    await db.commit()
    print(f"   {len(sector_map)} ta soha")
    return sector_map


async def seed_categories(db: AsyncSession) -> dict[str, int]:
    print("Kategoriyalar qo'shilmoqda...")
    cat_map = {}
    for data in CATEGORIES:
        existing = await db.execute(
            select(ProductCategory).where(ProductCategory.name == data["name"])
        )
        cat = existing.scalar_one_or_none()
        if not cat:
            cat = ProductCategory(**data)
            db.add(cat)
            await db.flush()
        cat_map[data["name"]] = cat.id
    await db.commit()
    print(f"   {len(cat_map)} ta kategoriya")
    return cat_map


async def seed_companies(db: AsyncSession, sector_map: dict[str, int]) -> dict[str, int]:
    print("Kompaniyalar qo'shilmoqda...")
    comp_map = {}
    for data in COMPANIES:
        existing = await db.execute(select(Company).where(Company.name == data["name"]))
        comp = existing.scalar_one_or_none()
        if not comp:
            comp = Company(
                name=data["name"],
                sector_id=sector_map[data["sector"]],
                founded_year=data["founded_year"],
                headquarters=data.get("headquarters"),
                website=data.get("website"),
            )
            db.add(comp)
            await db.flush()
        comp_map[data["name"]] = comp.id
    await db.commit()
    print(f"   {len(comp_map)} ta kompaniya")
    return comp_map


async def seed_branches(db: AsyncSession, comp_map: dict[str, int]) -> list[int]:
    print("Filiallar qo'shilmoqda...")
    branch_ids = []
    for comp_name, comp_id in comp_map.items():
        existing_q = await db.execute(
            select(Branch).where(Branch.company_id == comp_id)
        )
        existing_branches = existing_q.scalars().all()
        if existing_branches:
            branch_ids.extend([b.id for b in existing_branches])
            continue

        n_branches = random.randint(2, 5)
        for i in range(n_branches):
            city = random.choice(CITIES)
            street = random.choice(STREETS)
            name = f"{comp_name} {city} #{i + 1}"
            branch = Branch(
                company_id=comp_id,
                name=name,
                city=city,
                address=f"{street}, {random.randint(1, 200)}",
                opening_date=date(
                    random.randint(2010, 2024),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
            )
            db.add(branch)
            await db.flush()
            branch_ids.append(branch.id)
    await db.commit()
    print(f"   {len(branch_ids)} ta filial")
    return branch_ids


async def seed_products(db: AsyncSession, cat_map: dict[str, int]) -> list[int]:
    print("Mahsulotlar qo'shilmoqda...")
    product_ids = []
    for data in PRODUCTS:
        existing = await db.execute(select(Product).where(Product.name == data["name"]))
        product = existing.scalar_one_or_none()
        if not product:
            product = Product(
                name=data["name"],
                category_id=cat_map[data["category"]],
                price=data["price"],
                unit=data["unit"],
            )
            db.add(product)
            await db.flush()
        product_ids.append(product.id)
    await db.commit()
    print(f"   {len(product_ids)} ta mahsulot")
    return product_ids


async def seed_inventory(
    db: AsyncSession, branch_ids: list[int], product_ids: list[int]
) -> None:
    print("Ombor ma'lumotlari qo'shilmoqda...")
    count = 0
    for branch_id in branch_ids:
        selected_products = random.sample(product_ids, k=random.randint(8, 15))
        for product_id in selected_products:
            existing = await db.execute(
                select(Inventory).where(
                    Inventory.branch_id == branch_id,
                    Inventory.product_id == product_id,
                )
            )
            if existing.scalar_one_or_none():
                continue
            db.add(
                Inventory(
                    branch_id=branch_id,
                    product_id=product_id,
                    quantity=Decimal(str(random.randint(10, 500))),
                )
            )
            count += 1
    await db.commit()
    print(f"   {count} ta ombor yozuvi")


async def seed_sales(
    db: AsyncSession, branch_ids: list[int], product_ids: list[int]
) -> None:
    print("Sotuvlar qo'shilmoqda (so'nggi 90 kun)...")
    count = 0
    today = date.today()
    # Avval mahsulot narxlarini cache qilamiz
    price_cache = {}
    for pid in product_ids:
        p = await db.get(Product, pid)
        price_cache[pid] = p.price

    for branch_id in branch_ids:
        for day_offset in range(90):
            sale_date = today - timedelta(days=day_offset)
            n_sales = random.randint(3, 8)
            for _ in range(n_sales):
                product_id = random.choice(product_ids)
                qty = Decimal(str(random.randint(1, 20)))
                total = price_cache[product_id] * qty
                db.add(
                    Sale(
                        branch_id=branch_id,
                        product_id=product_id,
                        quantity=qty,
                        total_amount=total,
                        sale_date=sale_date,
                    )
                )
                count += 1
        # Har filial uchun alohida commit (memory tejash)
        await db.commit()
    print(f"   {count} ta sotuv")


async def seed_financial_reports(
    db: AsyncSession, comp_map: dict[str, int]
) -> None:
    print("Moliyaviy hisobotlar qo'shilmoqda...")
    count = 0
    years = [2024, 2025]
    for comp_name, comp_id in comp_map.items():
        for year in years:
            for month in range(1, 13):
                existing = await db.execute(
                    select(FinancialReport).where(
                        FinancialReport.company_id == comp_id,
                        FinancialReport.year == year,
                        FinancialReport.month == month,
                    )
                )
                if existing.scalar_one_or_none():
                    continue
                base = random.randint(800_000_000, 30_000_000_000)
                income = Decimal(str(base))
                expense = Decimal(str(int(base * random.uniform(0.6, 0.85))))
                profit = income - expense
                db.add(
                    FinancialReport(
                        company_id=comp_id,
                        year=year,
                        month=month,
                        income=income,
                        expense=expense,
                        net_profit=profit,
                    )
                )
                count += 1
    await db.commit()
    print(f"   {count} ta moliyaviy hisobot")


async def main() -> None:
    print("=" * 60)
    print("SEED DATA BOSHLANDI")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        sector_map = await seed_sectors(db)
        cat_map = await seed_categories(db)
        comp_map = await seed_companies(db, sector_map)
        branch_ids = await seed_branches(db, comp_map)
        product_ids = await seed_products(db, cat_map)
        await seed_inventory(db, branch_ids, product_ids)
        await seed_sales(db, branch_ids, product_ids)
        await seed_financial_reports(db, comp_map)

    await engine.dispose()
    print("=" * 60)
    print("SEED DATA TUGADI!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
