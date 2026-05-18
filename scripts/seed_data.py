"""Bazaga test ma'lumotlarini yuklash (CLI entry).

Ishlatish:
    python scripts/seed_data.py

Asosiy logika app/services/seed.py'da. Bu skript faqat
CLI orqali shu logikani chaqirish uchun.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import AsyncSessionLocal, engine  # noqa: E402
from app.services.seed import seed_all  # noqa: E402


async def main() -> None:
    print("=" * 60)
    print("SEED DATA BOSHLANDI")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        result = await seed_all(db, days_of_sales=30)

    await engine.dispose()

    print("=" * 60)
    print("SEED DATA TUGADI!")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
