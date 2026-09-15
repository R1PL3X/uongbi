"""
Presentation Layer - API endpoints cho Gio hang & Don hang (Sprint 2 - Epic 1).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.deps import getCurrentUser, requireRoles
from app.models.enums import VaiTro
from app.models.nguoi_dung import NguoiDung
from app.schemas.don_hang import DonHangCreateRequest, DonHangResponse
from app.services import don_hang_service

router = APIRouter(prefix="/api/donhang", tags=["DonHang"])


@router.post("", response_model=DonHangResponse, status_code=201)
def taoDonHang(
    payload: DonHangCreateRequest,
    db: Session = Depends(getDb),
    currentUser: NguoiDung = Depends(requireRoles(VaiTro.ROLE_BUYER)),
):
    """US09 - Xac nhan va tao don hang tu gio hang."""
    return don_hang_service.taoDonHang(db, currentUser.maNguoiDung, payload.items, payload.thoiGianNhan)


@router.get("/cua-toi", response_model=list[DonHangResponse])
def donCuaToi(db: Session = Depends(getDb), currentUser: NguoiDung = Depends(getCurrentUser)):
    """US12/US13 - Nhan ma don hang & theo doi trang thai don cua chinh minh."""
    return don_hang_service.layDonCuaNguoiDung(db, currentUser.maNguoiDung)


@router.get("/{maDonHang}", response_model=DonHangResponse)
def chiTietDonHang(
    maDonHang: int, db: Session = Depends(getDb), currentUser: NguoiDung = Depends(getCurrentUser)
):
    """US13 - Theo doi chi tiet trang thai 1 don hang."""
    return don_hang_service.layChiTietDon(db, maDonHang, currentUser)
