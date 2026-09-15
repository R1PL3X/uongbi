"""
Data Access Layer - Repository cho DonHang / ChiTietDonHang.
"""
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.models.don_hang import DonHang
from app.models.chi_tiet_don_hang import ChiTietDonHang


def create(db: Session, maNguoiDung: int, thoiGianNhan: datetime, tongTien: float, trangThai: str) -> DonHang:
    donHang = DonHang(
        maNguoiDung=maNguoiDung,
        thoiGianNhan=thoiGianNhan,
        tongTien=tongTien,
        trangThai=trangThai,
    )
    db.add(donHang)
    db.commit()
    db.refresh(donHang)
    return donHang


def addChiTiet(db: Session, maDonHang: int, maMon: int, soLuong: int, donGia: float) -> ChiTietDonHang:
    chiTiet = ChiTietDonHang(
        maDonHang=maDonHang,
        maMon=maMon,
        soLuong=soLuong,
        donGia=donGia,
        thanhTien=soLuong * donGia,
    )
    db.add(chiTiet)
    db.commit()
    db.refresh(chiTiet)
    return chiTiet


def getById(db: Session, maDonHang: int) -> DonHang | None:
    return (
        db.query(DonHang)
        .options(joinedload(DonHang.chiTietDonHangs), joinedload(DonHang.thanhToan))
        .filter(DonHang.maDonHang == maDonHang)
        .first()
    )


def getByNguoiDung(db: Session, maNguoiDung: int) -> list[DonHang]:
    return (
        db.query(DonHang)
        .options(joinedload(DonHang.chiTietDonHangs))
        .filter(DonHang.maNguoiDung == maNguoiDung)
        .order_by(DonHang.maDonHang.desc())
        .all()
    )


def getAll(db: Session) -> list[DonHang]:
    """Lich su toan bo don hang - dung cho Admin (US19)."""
    return (
        db.query(DonHang)
        .options(joinedload(DonHang.chiTietDonHangs))
        .order_by(DonHang.maDonHang.desc())
        .all()
    )


def getByTrangThai(db: Session, trangThais: list[str]) -> list[DonHang]:
    """Dung cho man hinh KDS - loc theo danh sach trang thai dang xu ly."""
    return (
        db.query(DonHang)
        .options(joinedload(DonHang.chiTietDonHangs))
        .filter(DonHang.trangThai.in_(trangThais))
        .order_by(DonHang.maDonHang.asc())
        .all()
    )


def getPendingExpired(db: Session, now: datetime, trangThaiChoThanhToan: str) -> list[DonHang]:
    """Lay cac don 'Cho thanh toan' da qua han (dung cho cronjob timeout)."""
    return (
        db.query(DonHang)
        .options(joinedload(DonHang.thanhToan))
        .filter(DonHang.trangThai == trangThaiChoThanhToan)
        .all()
    )


def updateTrangThai(db: Session, donHang: DonHang, trangThaiMoi: str) -> DonHang:
    donHang.trangThai = trangThaiMoi
    db.commit()
    db.refresh(donHang)
    return donHang


def setMaDonRutGon(db: Session, donHang: DonHang, maDonRutGon: str) -> DonHang:
    donHang.maDonRutGon = maDonRutGon
    db.commit()
    db.refresh(donHang)
    return donHang


def demTongSoDon(db: Session) -> int:
    return db.query(DonHang).count()
