"""
Data Access Layer - Repository cho ThanhToan.
"""
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.thanh_toan import ThanhToan


def create(
    db: Session,
    maDonHang: int,
    phuongThuc: str,
    soTien: float,
    trangThai: str,
    maQr: str,
    thoiHanThanhToan: datetime,
) -> ThanhToan:
    thanhToan = ThanhToan(
        maDonHang=maDonHang,
        phuongThuc=phuongThuc,
        soTien=soTien,
        trangThai=trangThai,
        maQr=maQr,
        thoiHanThanhToan=thoiHanThanhToan,
    )
    db.add(thanhToan)
    db.commit()
    db.refresh(thanhToan)
    return thanhToan


def getByMaDonHang(db: Session, maDonHang: int) -> ThanhToan | None:
    return db.query(ThanhToan).filter(ThanhToan.maDonHang == maDonHang).first()


def updateTrangThai(db: Session, thanhToan: ThanhToan, trangThaiMoi: str, ngayThanhToan=None) -> ThanhToan:
    thanhToan.trangThai = trangThaiMoi
    if ngayThanhToan is not None:
        thanhToan.ngayThanhToan = ngayThanhToan
    db.commit()
    db.refresh(thanhToan)
    return thanhToan
