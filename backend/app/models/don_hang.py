"""
Data Access Layer - ORM Model: DonHang
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base
from app.models.enums import TrangThaiDonHang


class DonHang(Base):
    __tablename__ = "don_hang"

    maDonHang = Column(Integer, primary_key=True, index=True, autoincrement=True)
    maNguoiDung = Column(Integer, ForeignKey("nguoi_dung.maNguoiDung"), nullable=False)
    ngayDat = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    tongTien = Column(Float, nullable=False, default=0)
    trangThai = Column(String(20), nullable=False, default=TrangThaiDonHang.CHO_THANH_TOAN)

    # Ma don rut gon de khach dung khi lay do, VD "#001"
    maDonRutGon = Column(String(20), nullable=True, index=True)
    # Khung gio nhan mon (US10) - phai trong gio hoat dong cua Canteen
    thoiGianNhan = Column(DateTime, nullable=False)

    # 1 NguoiDung - Nhieu DonHang
    nguoiDung = relationship("NguoiDung", back_populates="donHangs")
    # 1 DonHang - Nhieu ChiTietDonHang
    chiTietDonHangs = relationship(
        "ChiTietDonHang", back_populates="donHang", cascade="all, delete-orphan"
    )
    # 1 DonHang - 1 ThanhToan
    thanhToan = relationship(
        "ThanhToan", back_populates="donHang", uselist=False, cascade="all, delete-orphan"
    )
