# Statistics Platform API

Restoran va Supermarket tarmoqlarini statistik tahlil qiluvchi REST API.

**Tech Stack:** FastAPI · PostgreSQL · SQLAlchemy 2.0 (async) · Alembic · Pydantic v2 · Docker · GitHub Actions · Railway

---

## Loyiha haqida

Bu API O'zbekiston bozoridagi yirik **restoran** va **supermarket** tarmoqlari bo'yicha:
- Kompaniyalar va filiallar
- Mahsulotlar va omborlar
- Sotuvlar
- Moliyaviy hisobotlar

ma'lumotlarini boshqaradi va statistik tahlillarni taqdim etadi.

### Qamrov

| Soha | Kompaniyalar |
|------|--------------|
| **Restoran** | Evos, Max Way, Bellissimo Pizza, Rayhon, Sette Bello |
| **Supermarket** | Korzinka, Havas, Olma, Makro, Carrefour |

---

## Loyiha strukturasi

```
statistics-platform/
├── app/
│   ├── api/v1/          # API routerlari (CRUD + stats)
│   ├── core/            # Config va security
│   ├── db/              # SQLAlchemy base, session
│   ├── models/          # 9 ta SQLAlchemy model
│   ├── schemas/         # Pydantic schemalar
│   └── main.py          # FastAPI entry point
├── alembic/             # Database migrations
├── scripts/             # seed_data.py
├── tests/               # pytest testlari
├── .github/workflows/   # CI/CD
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── alembic.ini
```

---

## API endpointlar

### CRUD (har model uchun 5 ta endpoint):

```
GET    /api/v1/{resource}/           # ro'yxat
GET    /api/v1/{resource}/{id}       # bitta zapis
POST   /api/v1/{resource}/           # yangi
PATCH  /api/v1/{resource}/{id}       # yangilash
DELETE /api/v1/{resource}/{id}       # o'chirish
```

Resurslar: `sectors`, `companies`, `branches`, `product-categories`, `products`, `inventory`, `sales`, `financial-reports`, `users`

### Statistik endpointlar:

| Endpoint | Vazifasi |
|----------|----------|
| `GET /api/v1/stats/income/yearly` | Yillik kirim |
| `GET /api/v1/stats/income/monthly` | Oylik kirim |
| `GET /api/v1/stats/top-products` | Eng ko'p sotilgan mahsulotlar |
| `GET /api/v1/stats/inventory-remaining` | Ombordagi qoldiq |
| `GET /api/v1/stats/compare-companies` | Tarmoqlar taqqoslash |
| `GET /api/v1/stats/category-share` | Kategoriya ulushi |
| `GET /api/v1/stats/growth` | O'sish dinamikasi |

---

## Lokal ishga tushirish

### 1. Klon va virtual env

```bash
git clone <repo-url>
cd statistics-platform
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# yoki: source venv/bin/activate   # Linux/Mac
```

### 2. Kutubxonalar

```bash
pip install -r requirements.txt
```

### 3. `.env` faylini yaratish

`.env.example` ni nusxalab `.env` qiling va o'z ma'lumotlaringiz bilan to'ldiring.

### 4. Database migration

```bash
alembic upgrade head
```

### 5. Seed data (ixtiyoriy)

```bash
python scripts/seed_data.py
```

### 6. Server ishga tushirish

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

---

## Docker bilan ishga tushirish

```bash
docker compose up --build
```

API: http://localhost:8000/docs

---

## CI/CD

GitHub Actions har push'da quyidagilarni bajaradi:

1. **Lint** — ruff
2. **Migration** — alembic upgrade head
3. **Tests** — pytest
4. **Build** — Docker image
5. **Deploy** — Railway auto-deploy

---

## Deploy (Railway)

1. GitHub repo'ni Railway'ga ulanadi
2. PostgreSQL plugin qo'shiladi
3. Environment variables o'rnatiladi
4. Push qilingan zahoti — auto deploy

Public URL: `https://<your-app>.railway.app/docs`

---

## Texnologiyalar

- **Python 3.12**
- **FastAPI 0.115+**
- **SQLAlchemy 2.0** (async)
- **Asyncpg** — async PostgreSQL driver
- **Alembic** — migrations
- **Pydantic v2** — validation
- **Docker** — containerization
- **GitHub Actions** — CI/CD

---

## Litsenziya

MIT
