"""
Presentation Layer - Pydantic Schemas cho Cart/DonHang.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):
    maMon: int
    soLuong: int = Field(..., gt=0)


class DonHangCreateRequest(BaseModel):
    items: list[CartItemRequest]
    thoiGianNhan: datetime  # khung gio nhan mon, phai trong 7:00 - 18:00


class ChiTietDonHangResponse(BaseModel):
    maChiTiet: int
    maMon: int
    tenMon: str
    soLuong: int
    donGia: float
    thanhTien: float

    class Config:
        from_attributes = True


class DonHangResponse(BaseModel):
    maDonHang: int
    maDonRutGon: str | None
    maNguoiDung: int
    ngayDat: datetime
    thoiGianNhan: datetime
    tongTien: float
    trangThai: str
    chiTietDonHangs: list[ChiTietDonHangResponse] = []

    class Config:
        from_attributes = True


class CapNhatTrangThaiDonHangRequest(BaseModel):
    trangThaiMoi: str
