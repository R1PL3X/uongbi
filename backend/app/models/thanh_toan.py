"""
Data Access Layer - ORM Model: ThanhToan
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base
from app.models.enums import TrangThaiThanhToan


class ThanhToan(Base):
    __tablename__ = "thanh_toan"

    maThanhToan = Column(Integer, primary_key=True, index=True, autoincrement=True)
    maDonHang = Column(Integer, ForeignKey("don_hang.maDonHang"), unique=True, nullable=False)
    phuongThuc = Column(String(20), nullable=False)
    soTien = Column(Float, nullable=False)
    trangThai = Column(String(20), nullable=False, default=TrangThaiThanhToan.CHO_XU_LY)

    maQr = Column(String(100), nullable=True)  # ma QR mock, vo hieu hoa khi het han/da dung
    thoiHanThanhToan = Column(DateTime, nullable=False)  # het han neu qua moc nay ma chua thanh toan
    ngayThanhToan = Column(DateTime, nullable=True)  # thoi diem webhook bao thanh cong
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    donHang = relationship("DonHang", back_populates="thanhToan")
