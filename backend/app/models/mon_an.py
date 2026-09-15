"""
Data Access Layer - ORM Model: MonAn
"""
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import TrangThaiMonAn


class MonAn(Base):
    __tablename__ = "mon_an"

    maMon = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenMon = Column(String(150), nullable=False)
    donGia = Column(Float, nullable=False)
    moTa = Column(Text, nullable=True)
    hinhAnh = Column(String(500), nullable=True)  # URL/path anh thumbnail
    trangThai = Column(String(20), nullable=False, default=TrangThaiMonAn.CON_HANG)

    # 1 MonAn - Nhieu ChiTietDonHang
    chiTietDonHangs = relationship("ChiTietDonHang", back_populates="monAn")
    # 1 MonAn - Nhieu DanhGia
    danhGias = relationship("DanhGia", back_populates="monAn")
