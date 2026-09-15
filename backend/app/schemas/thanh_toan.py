"""
Presentation Layer - Pydantic Schemas cho ThanhToan (QR mock).
"""
from datetime import datetime
from pydantic import BaseModel


class ThanhToanResponse(BaseModel):
    maThanhToan: int
    maDonHang: int
    phuongThuc: str
    soTien: float
    trangThai: str
    maQr: str | None
    qrImageBase64: str  # anh QR mock (SVG data-uri) de FE hien thi truc tiep
    thoiHanThanhToan: datetime

    class Config:
        from_attributes = True


class WebhookThanhToanRequest(BaseModel):
    """Mock callback tu cong thanh toan (VietQR/Momo) bao ket qua giao dich."""
    maDonHang: int
    maQr: str
    ketQua: str  # "THANH_CONG" | "THAT_BAI"
