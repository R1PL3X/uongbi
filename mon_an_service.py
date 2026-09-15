"""
Business/Service Layer - logic nghiep vu cho MonAn (menu cong khai + quan tri Admin).
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import TrangThaiMonAn
from app.repositories import mon_an_repository


def danhSachMenuCongKhai(db: Session):
    """US03/US05 - Danh sach mon an cho khach xem (khong bao gom mon da xoa mem)."""
    return mon_an_repository.getAllVisible(db)


def chiTietMon(db: Session, maMon: int):
    """US04 - Chi tiet 1 mon an."""
    monAn = mon_an_repository.getById(db, maMon)
    if not monAn or monAn.trangThai == TrangThaiMonAn.DA_XOA:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay mon an")
    return monAn


def danhSachMenuAdmin(db: Session):
    """US17/US18 - Admin xem toan bo mon (ke ca da an) de quan ly."""
    return mon_an_repository.getAllForAdmin(db)


def taoMonMoi(db: Session, tenMon: str, donGia: float, moTa: str | None, hinhAnh: str | None):
    """TC54 - Tao moi mon an."""
    return mon_an_repository.create(db, tenMon, donGia, moTa, hinhAnh)


def _layMonHopLe(db: Session, maMon: int):
    monAn = mon_an_repository.getById(db, maMon)
    if not monAn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay mon an")
    return monAn


def capNhatMon(
    db: Session,
    maMon: int,
    tenMon: str | None,
    donGia: float | None,
    moTa: str | None,
    hinhAnh: str | None,
    trangThai: str | None,
):
    """TC55 - Cap nhat gia va trang thai Con/Het hang.
    Khi Admin doi trangThai thanh HET_HANG, lan GET menu tiep theo cua khach
    se ngay lap tuc tra ve trang thai moi (khong cache), FE se hien nut 'HET HANG'
    va chan khong cho them vao gio."""
    monAn = _layMonHopLe(db, maMon)

    if trangThai is not None and trangThai not in (TrangThaiMonAn.CON_HANG, TrangThaiMonAn.HET_HANG):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="trangThai chi duoc phep la CON_HANG hoac HET_HANG",
        )

    return mon_an_repository.update(
        db, monAn, tenMon=tenMon, donGia=donGia, moTa=moTa, hinhAnh=hinhAnh, trangThai=trangThai
    )


def xoaMon(db: Session, maMon: int):
    """TC56 - Xoa mem (Soft Delete): chi an mon khoi menu, khong xoa cung khoi DB,
    de khong lam anh huong du lieu Lich su don hang cu da tham chieu toi mon nay."""
    monAn = _layMonHopLe(db, maMon)
    return mon_an_repository.softDelete(db, monAn)


def toggleTrangThaiNhanh(db: Session, maMon: int):
    """Quick Action tren KDS: nhan vien bep gat nhanh Con/Het hang khong can vao Admin."""
    monAn = _layMonHopLe(db, maMon)
    trangThaiMoi = (
        TrangThaiMonAn.HET_HANG if monAn.trangThai == TrangThaiMonAn.CON_HANG else TrangThaiMonAn.CON_HANG
    )
    return mon_an_repository.update(db, monAn, trangThai=trangThaiMoi)
