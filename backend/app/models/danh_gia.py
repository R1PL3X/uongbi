"""
Data Access Layer - ORM Model: DanhGia
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class DanhGia(Base):
    __tablename__ = "danh_gia"

    maDanhGia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    maNguoiDung = Column(Integer, ForeignKey("nguoi_dung.maNguoiDung"), nullable=False)
    maMon = Column(Integer, ForeignKey("mon_an.maMon"), nullable=False)
    noiDung = Column(Text, nullable=True)
    soSao = Column(Integer, nullable=False, default=5)  # 1-5 sao
    ngayDanhGia = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    nguoiDung = relationship("NguoiDung", back_populates="danhGias")
    monAn = relationship("MonAn", back_populates="danhGias")
