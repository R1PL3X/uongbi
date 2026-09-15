"""
Data Access Layer - ORM Model: ChiTietDonHang
"""
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChiTietDonHang(Base):
    __tablename__ = "chi_tiet_don_hang"

    maChiTiet = Column(Integer, primary_key=True, index=True, autoincrement=True)
    maDonHang = Column(Integer, ForeignKey("don_hang.maDonHang"), nullable=False)
    maMon = Column(Integer, ForeignKey("mon_an.maMon"), nullable=False)
    soLuong = Column(Integer, nullable=False, default=1)
    donGia = Column(Float, nullable=False)  # snapshot gia tai thoi diem dat, tranh anh huong khi Admin doi gia sau nay
    thanhTien = Column(Float, nullable=False)  # = soLuong * donGia

    donHang = relationship("DonHang", back_populates="chiTietDonHangs")
    monAn = relationship("MonAn", back_populates="chiTietDonHangs")

    @property
    def tenMon(self) -> str:
        """Tien ich cho Presentation Layer: lay ten mon tu quan he MonAn de tra ve
        cung luc voi chi tiet don hang, khong can FE goi them API rieng."""
        return self.monAn.tenMon if self.monAn else ""
