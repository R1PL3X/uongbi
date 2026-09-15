"""
Presentation Layer - API endpoints cho Menu cong khai (Sprint 1 - Epic 2).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.schemas.mon_an import MonAnResponse
from app.services import mon_an_service

router = APIRouter(prefix="/api/menu", tags=["Menu"])


@router.get("", response_model=list[MonAnResponse])
def danhSachMenu(db: Session = Depends(getDb)):
    """US03/US05 - GET /api/menu tra ve danh sach mon an day du thuoc tinh, gom trangThai
    de FE hien thi dung Con hang / Het hang."""
    return mon_an_service.danhSachMenuCongKhai(db)


@router.get("/{maMon}", response_model=MonAnResponse)
def chiTietMon(maMon: int, db: Session = Depends(getDb)):
    """US04 - Xem chi tiet 1 mon an (ten, hinh anh, gia, mo ta)."""
    return mon_an_service.chiTietMon(db, maMon)
