"""
Presentation Layer - API endpoints cho KDS - Kitchen Display System (Sprint 2 - Epic 3).
Chi ROLE_STAFF va ROLE_ADMIN duoc truy cap.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.deps import requireRoles
from app.models.enums import VaiTro, TrangThaiDonHang
from app.models.nguoi_dung import NguoiDung
from app.schemas.don_hang import DonHangResponse, CapNhatTrangThaiDonHangRequest
from app.schemas.mon_an import MonAnResponse
from app.services import don_hang_service, mon_an_service

router = APIRouter(prefix="/api/kds", tags=["KDS"])

# Cac trang thai don hang ma nhan vien bep can theo doi tren man hinh KDS
TRANG_THAI_KDS_THEO_DOI = [
    TrangThaiDonHang.DA_THANH_TOAN,
    TrangThaiDonHang.DANG_CHUAN_BI,
    TrangThaiDonHang.SAN_SANG_NHAN,
]


@router.get("/orders", response_model=list[DonHangResponse])
def donHangChoBep(
    db: Session = Depends(getDb),
    _currentUser: NguoiDung = Depends(requireRoles(VaiTro.ROLE_STAFF, VaiTro.ROLE_ADMIN)),
):
    """US14 - Xem cac don hang moi (da thanh toan) can chuan bi. FE nen goi lai
    (poll) endpoint nay dinh ky de tu dong dong bo cac don bi lo khi mat mang (Risk #5)."""
    return don_hang_service.layDonTheoTrangThai(db, TRANG_THAI_KDS_THEO_DOI)


@router.patch("/orders/{maDonHang}/status", response_model=DonHangResponse)
def capNhatTrangThaiDon(
    maDonHang: int,
    payload: CapNhatTrangThaiDonHangRequest,
    db: Session = Depends(getDb),
    _currentUser: NguoiDung = Depends(requireRoles(VaiTro.ROLE_STAFF, VaiTro.ROLE_ADMIN)),
):
    """US15 - Cap nhat trang thai don hang tuan tu (TC41-TC45)."""
    return don_hang_service.capNhatTrangThaiDonHang(db, maDonHang, payload.trangThaiMoi)


@router.patch("/mon/{maMon}/toggle", response_model=MonAnResponse)
def toggleTrangThaiMon(
    maMon: int,
    db: Session = Depends(getDb),
    _currentUser: NguoiDung = Depends(requireRoles(VaiTro.ROLE_STAFF, VaiTro.ROLE_ADMIN)),
):
    """US16 - Quick Action: nhan vien bep bat/tat nhanh Con/Het hang tu KDS."""
    return mon_an_service.toggleTrangThaiNhanh(db, maMon)
