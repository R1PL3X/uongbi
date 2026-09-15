"""
Data Access Layer - ORM Model: NguoiDung
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    maNguoiDung = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hoTen = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    matKhau = Column(String(255), nullable=False)  # luu ban bam (hash), khong luu plaintext
    vaiTro = Column(String(20), nullable=False)  # ROLE_BUYER | ROLE_STAFF | ROLE_ADMIN

    # 1 NguoiDung - Nhieu DonHang
    donHangs = relationship("DonHang", back_populates="nguoiDung")
    # 1 NguoiDung - Nhieu DanhGia
    danhGias = relationship("DanhGia", back_populates="nguoiDung")
