"""
Business/Service Layer - logic nghiep vu cho Gio hang & Tao don hang (Sprint 2 - Epic 1)
va State Machine cho KDS (Sprint 2 - Epic 3).
"""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import TrangThaiMonAn, TrangThaiDonHang
from app.repositories import mon_an_repository, don_hang_repository


def _kiemTraKhungGioNhan(thoiGianNhan: datetime):
    """TC24, TC25 - Khung gio nhan bat buoc phai nam trong gio hoat dong cua Canteen."""
    gio = thoiGianNhan.hour + thoiGianNhan.minute / 60
    if not (settings.CANTEEN_OPEN_HOUR <= gio <= settings.CANTEEN_CLOSE_HOUR):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Khung gio nhan mon phai nam trong gio hoat dong cua Canteen "
                f"({settings.CANTEEN_OPEN_HOUR}:00 - {settings.CANTEEN_CLOSE_HOUR}:00)"
            ),
        )


def taoDonHang(db: Session, maNguoiDung: int, items: list, thoiGianNhan: datetime):
    """
    US06-US10 - Tao don hang tu gio hang.
    - Ngoai le 1 (TC14): kiem tra lai trang thai cac mon trong gio, neu mon nao
      'Het hang' phai bao loi, chan tao don, yeu cau nguoi dung xoa mon do khoi gio.
    - TC24/TC25: bat buoc chon khung gio nhan, phai trong gio hoat dong.
    - Tinh toan chinh xac tongTien = Tong (soLuong * donGia). Khoi tao don voi
      trang thai mac dinh 'Cho thanh toan'.
    """
    if not items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gio hang dang trong")

    _kiemTraKhungGioNhan(thoiGianNhan)

    monHetHang = []
    danhSachMon = []
    for item in items:
        monAn = mon_an_repository.getById(db, item.maMon)
        if not monAn or monAn.trangThai == TrangThaiMonAn.DA_XOA:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Mon an ma {item.maMon} khong ton tai"
            )
        if monAn.trangThai == TrangThaiMonAn.HET_HANG:
            monHetHang.append(monAn.tenMon)
        danhSachMon.append((monAn, item.soLuong))

    if monHetHang:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Cac mon sau da HET HANG, vui long xoa khoi gio truoc khi dat: "
                + ", ".join(monHetHang)
            ),
        )

    tongTien = sum(monAn.donGia * soLuong for monAn, soLuong in danhSachMon)

    donHang = don_hang_repository.create(
        db,
        maNguoiDung=maNguoiDung,
        thoiGianNhan=thoiGianNhan,
        tongTien=tongTien,
        trangThai=TrangThaiDonHang.CHO_THANH_TOAN,
    )

    for monAn, soLuong in danhSachMon:
        don_hang_repository.addChiTiet(db, donHang.maDonHang, monAn.maMon, soLuong, monAn.donGia)

    return don_hang_repository.getById(db, donHang.maDonHang)


def _layDonHopLe(db: Session, maDonHang: int):
    donHang = don_hang_repository.getById(db, maDonHang)
    if not donHang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay don hang")
    return donHang


def layDonCuaNguoiDung(db: Session, maNguoiDung: int):
    return don_hang_repository.getByNguoiDung(db, maNguoiDung)


def layChiTietDon(db: Session, maDonHang: int, nguoiDungHienTai):
    """Nguoi mua chi duoc xem don cua chinh minh; Staff/Admin xem duoc tat ca."""
    from app.models.enums import VaiTro

    donHang = _layDonHopLe(db, maDonHang)
    if nguoiDungHienTai.vaiTro == VaiTro.ROLE_BUYER and donHang.maNguoiDung != nguoiDungHienTai.maNguoiDung:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong co quyen xem don hang nay")
    return donHang


def layDonTheoTrangThai(db: Session, trangThais: list[str]):
    """Man hinh KDS (US14) - danh sach don moi can chuan bi."""
    return don_hang_repository.getByTrangThai(db, trangThais)


def capNhatTrangThaiDonHang(db: Session, maDonHang: int, trangThaiMoi: str):
    """
    US15 - Cap nhat trang thai don hang.
    TC41-TC45 - Order State Machine: trang thai khong duoc nhay coc, bat buoc di
    dung tuan tu theo NEXT_STATE da dinh nghia trong TrangThaiDonHang.
    """
    donHang = _layDonHopLe(db, maDonHang)

    if trangThaiMoi not in TrangThaiDonHang.NEXT_STATE.get(donHang.trangThai, set()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Khong the chuyen trang thai tu '{donHang.trangThai}' sang '{trangThaiMoi}'. "
                f"Luong bat buoc: Cho thanh toan -> Da thanh toan -> Dang chuan bi -> "
                f"San sang nhan -> Hoan thanh."
            ),
        )

    return don_hang_repository.updateTrangThai(db, donHang, trangThaiMoi)


def sinhMaDonRutGon(db: Session) -> str:
    """Sinh ma don ngan gon kieu #001 de khach dung khi lay do."""
    tongSoDon = don_hang_repository.demTongSoDon(db)
    return f"#{tongSoDon:03d}"
