"""
Presentation Layer - API endpoints cho QR Payment mock (Sprint 2 - Epic 2).
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.deps import getCurrentUser, requireRoles
from app.models.enums import VaiTro, PhuongThucThanhToan
from app.models.nguoi_dung import NguoiDung
from app.schemas.thanh_toan import ThanhToanResponse, WebhookThanhToanRequest
from app.schemas.don_hang import DonHangResponse
from app.services import thanh_toan_service

router = APIRouter(prefix="/api/thanhtoan", tags=["ThanhToan"])


@router.post("/{maDonHang}/qr", response_model=ThanhToanResponse)
def sinhQrThanhToan(
    maDonHang: int,
    phuongThuc: str = Query(default=PhuongThucThanhToan.VIETQR),
    db: Session = Depends(getDb),
    currentUser: NguoiDung = Depends(requireRoles(VaiTro.ROLE_BUYER)),
):
    """US11 - Sinh ma QR (VietQR/Momo mock) chua dung so tien tong don hang."""
    thanhToan, qrImageBase64 = thanh_toan_service.taoQrThanhToan(db, maDonHang, phuongThuc, currentUser)
    return ThanhToanResponse(
        maThanhToan=thanhToan.maThanhToan,
        maDonHang=thanhToan.maDonHang,
        phuongThuc=thanhToan.phuongThuc,
        soTien=thanhToan.soTien,
        trangThai=thanhToan.trangThai,
        maQr=thanhToan.maQr,
        qrImageBase64=qrImageBase64,
        thoiHanThanhToan=thanhToan.thoiHanThanhToan,
    )


@router.post("/webhook", response_model=DonHangResponse)
def webhookThanhToan(payload: WebhookThanhToanRequest, db: Session = Depends(getDb)):
    """
    Mock Callback tu cong thanh toan (khong yeu cau JWT vi day la endpoint noi bo
    cong thanh toan goi vao, giong webhook thuc te). Dung de gia lap nut
    'Da thanh toan (demo)' tren giao dien FE.
    """
    return thanh_toan_service.xuLyWebhookThanhToan(db, payload.maDonHang, payload.maQr, payload.ketQua)
