"""
Business/Service Layer - logic nghiep vu cho Dang ky / Dang nhap / Quen mat khau.
"""
import secrets

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hashPassword, verifyPassword, createAccessToken
from app.models.enums import VaiTro
from app.repositories import nguoi_dung_repository

# Sidebar dieu huong FE tuong ung voi tung Role sau khi dang nhap
REDIRECT_BY_ROLE = {
    VaiTro.ROLE_BUYER: "/menu.html",
    VaiTro.ROLE_STAFF: "/kds.html",
    VaiTro.ROLE_ADMIN: "/admin/dashboard.html",
}


def dangKy(db: Session, hoTen: str, email: str, matKhau: str, vaiTro: str):
    if vaiTro not in VaiTro.ALL:
        vaiTro = VaiTro.ROLE_BUYER

    # Email dang ky khong duoc trung lap
    nguoiDungTonTai = nguoi_dung_repository.getByEmail(db, email)
    if nguoiDungTonTai:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email da duoc su dung, vui long chon email khac",
        )

    matKhauHash = hashPassword(matKhau)
    nguoiDung = nguoi_dung_repository.create(db, hoTen, email, matKhauHash, vaiTro)
    return nguoiDung


def dangNhap(db: Session, email: str, matKhau: str):
    nguoiDung = nguoi_dung_repository.getByEmail(db, email)

    # Sai email hoac sai mat khau deu tra chung 1 thong bao (Ref TC02) de tranh
    # lo thong tin email nao da ton tai trong he thong.
    if not nguoiDung or not verifyPassword(matKhau, nguoiDung.matKhau):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai thong tin dang nhap",
        )

    accessToken = createAccessToken(data={"sub": str(nguoiDung.maNguoiDung), "vaiTro": nguoiDung.vaiTro})
    redirectTo = REDIRECT_BY_ROLE.get(nguoiDung.vaiTro, "/menu.html")
    return accessToken, nguoiDung, redirectTo


def quenMatKhau(db: Session, email: str):
    nguoiDung = nguoi_dung_repository.getByEmail(db, email)
    if not nguoiDung:
        # Khong tiet lo email co ton tai hay khong, tranh do tham thong tin tai khoan
        return "Neu email ton tai trong he thong, mat khau tam thoi da duoc tao.", None

    # Demo/dev: he thong chua noi voi dich vu gui email that su nen tao mat khau
    # tam thoi va tra ve truc tiep de nguoi dung/QA co the test lai luong dang nhap.
    # Trong moi truong production, buoc nay phai gui qua email, KHONG tra ve API.
    matKhauTamThoi = secrets.token_urlsafe(6)
    nguoi_dung_repository.updateMatKhau(db, nguoiDung, hashPassword(matKhauTamThoi))
    return "Mat khau tam thoi da duoc tao, vui long dang nhap va doi lai mat khau.", matKhauTamThoi
