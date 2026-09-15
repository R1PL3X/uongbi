"""
Presentation Layer - Entry point cua ung dung FastAPI.
Khoi tao DB, dang ky router, cau hinh CORS, phuc vu Frontend tinh (HTML/CSS/JS)
va chay ngam background job xu ly timeout thanh toan.
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app import models  # noqa: F401 - dam bao models duoc dang ky vao Base.metadata
from app.jobs.payment_timeout_job import vongLapKiemTraTimeout
from app.routers import auth, menu, don_hang, thanh_toan, kds, admin

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khoi tao bang trong DB neu chua ton tai
    Base.metadata.create_all(bind=engine)
    # Chay ngam cronjob quet don timeout thanh toan (TC35)
    task = asyncio.create_task(vongLapKiemTraTimeout())
    yield
    task.cancel()


app = FastAPI(
    title=settings.APP_NAME,
    description="API cho du an MVP Uong Bi GO - He thong dat mon Canteen",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dang ky cac router API (Presentation Layer)
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(don_hang.router)
app.include_router(thanh_toan.router)
app.include_router(kds.router)
app.include_router(admin.router)


@app.get("/api/health")
def healthCheck():
    return {"status": "ok", "app": settings.APP_NAME}


# Phuc vu Frontend tinh (HTML/CSS/JS thuan) tu thu muc ../frontend
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
