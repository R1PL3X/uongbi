"""
Business/Service Layer - logic nghiep vu QR Payment mock & Order tracking (Sprint 2 - Epic 2).
"""
import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import TrangThaiDonHang, TrangThaiThanhToan, PhuongThucThanhToan
from app.repositories import don_hang_repository, thanh_toan_repository
from app.services.don_hang_service import sinhMaDonRutGon


def _svgQrMockBase64(noiDung: str) -> str:
    """
    Sinh 1 anh SVG gia lap QR code (khong phai QR that, chi de demo giao dien):
    ve mot luoi o vuong den/trang duoc xac dinh boi hash cua noi dung, nhin
    truc quan giong ma QR that de FE hien thi.
    """
    kichThuocLuoi = 21
    hashBytes = hashlib.sha256(noiDung.encode()).digest()
    bits = []
    for b in hashBytes:
        bits.extend([(b >> i) & 1 for i in range(8)])
    while len(bits) < kichThuocLuoi * kichThuocLuoi:
        bits.extend(bits)

    o = 10  # kich thuoc moi o vuong (px)
    svgParts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{kichThuocLuoi*o}" height="{kichThuocLuoi*o}">',
        f'<rect width="100%" height="100%" fill="white"/>',
    ]
    idx = 0
    for row in range(kichThuocLuoi):
        for col in range(kichThuocLuoi):
            # 3 goc QR luon la khoi vuong dac (finder pattern) de nhin giong QR that
            isFinderCorner = (row < 7 and col < 7) or (row < 7 and col >= kichThuocLuoi - 7) or (
                row >= kichThuocLuoi - 7 and col < 7
            )
            if isFinderCorner:
                inBorder = row % 7 in (0, 6) or col % 7 in (0, 6) if row < 7 else True
                den = True
            else:
                den = bits[idx] == 1
            idx += 1
            if den:
                svgParts.append(f'<rect x="{col*o}" y="{row*o}" width="{o}" height="{o}" fill="black"/>')
    svgParts.append("</svg>")
    svg = "".join(svgParts)
    encoded = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{encoded}"


def taoQrThanhToan(db: Session, maDonHang: int, phuongThuc: str, nguoiDungHienTai):
    """
    US11 - Sinh QR thanh toan (VietQR/Momo mock).
    TC29/TC30 - QR phai chua dung so tien tong cua don hang.
    """
    donHang = don_hang_repository.getById(db, maDonHang)
    if not donHang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay don hang")

    if donHang.maNguoiDung != nguoiDungHienTai.maNguoiDung:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong co quyen thanh toan don nay")

    if donHang.trangThai != TrangThaiDonHang.CHO_THANH_TOAN:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Don hang dang o trang thai '{donHang.trangThai}', khong the sinh QR thanh toan moi",
        )

    if phuongThuc not in (PhuongThucThanhToan.VIETQR, PhuongThucThanhToan.MOMO):
        phuongThuc = PhuongThucThanhToan.VIETQR

    maQr = secrets.token_hex(8)
    thoiHan = datetime.now(timezone.utc) + timedelta(minutes=settings.PAYMENT_TIMEOUT_MINUTES)

    thanhToanCu = thanh_toan_repository.getByMaDonHang(db, maDonHang)
    if thanhToanCu and thanhToanCu.trangThai == TrangThaiThanhToan.CHO_XU_LY:
        # Da co QR dang cho xu ly -> vo hieu hoa QR cu, tao QR moi thay the
        thanh_toan_repository.updateTrangThai(db, thanhToanCu, TrangThaiThanhToan.HET_HAN)

    thanhToan = thanh_toan_repository.create(
        db,
        maDonHang=maDonHang,
        phuongThuc=phuongThuc,
        soTien=donHang.tongTien,
        trangThai=TrangThaiThanhToan.CHO_XU_LY,
        maQr=maQr,
        thoiHanThanhToan=thoiHan,
    )

    noiDungQr = f"{phuongThuc}|{maDonHang}|{thanhToan.soTien}|{maQr}"
    qrImageBase64 = _svgQrMockBase64(noiDungQr)

    return thanhToan, qrImageBase64


def xuLyWebhookThanhToan(db: Session, maDonHang: int, maQr: str, ketQua: str):
    """
    Mock callback tu cong thanh toan.
    Ngoai le 6 (TC37) - Chong thanh toan trung: neu don da 'Da thanh toan', tu choi
    moi request cap nhat thanh toan moi cho ma don do.
    """
    donHang = don_hang_repository.getById(db, maDonHang)
    if not donHang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay don hang")

    if donHang.trangThai == TrangThaiDonHang.DA_THANH_TOAN or donHang.trangThai not in (
        TrangThaiDonHang.CHO_THANH_TOAN,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Don hang da o trang thai '{donHang.trangThai}', tu choi cap nhat thanh toan trung lap",
        )

    thanhToan = thanh_toan_repository.getByMaDonHang(db, maDonHang)
    if not thanhToan or thanhToan.maQr != maQr:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ma QR khong hop le")

    if thanhToan.trangThai != TrangThaiThanhToan.CHO_XU_LY:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ma QR nay da o trang thai '{thanhToan.trangThai}', khong the xu ly lai",
        )

    now = datetime.now(timezone.utc)
    thoiHan = thanhToan.thoiHanThanhToan
    if thoiHan.tzinfo is None:
        thoiHan = thoiHan.replace(tzinfo=timezone.utc)
    if now > thoiHan:
        thanh_toan_repository.updateTrangThai(db, thanhToan, TrangThaiThanhToan.HET_HAN)
        don_hang_repository.updateTrangThai(db, donHang, TrangThaiDonHang.DA_HUY)
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Ma QR da het han, don hang da bi huy")

    if ketQua == TrangThaiThanhToan.THANH_CONG:
        thanh_toan_repository.updateTrangThai(db, thanhToan, TrangThaiThanhToan.THANH_CONG, ngayThanhToan=now)
        don_hang_repository.updateTrangThai(db, donHang, TrangThaiDonHang.DA_THANH_TOAN)
        # Sinh ma don rut gon de khach dung khi lay do (VD #001)
        don_hang_repository.setMaDonRutGon(db, donHang, sinhMaDonRutGon(db))
        # TC39 - Ngay khi don sang 'Da thanh toan', don se xuat hien tren man hinh
        # KDS trong lan poll/fetch tiep theo cua nhan vien bep (xem routers/kds.py).
    else:
        thanh_toan_repository.updateTrangThai(db, thanhToan, TrangThaiThanhToan.THAT_BAI)

    return don_hang_repository.getById(db, maDonHang)
