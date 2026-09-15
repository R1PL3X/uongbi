"""
Data Access Layer - Repository cho NguoiDung.
Chi chua thao tac truy van/ghi DB, khong chua logic nghiep vu.
"""
from sqlalchemy.orm import Session

from app.models.nguoi_dung import NguoiDung


def getByEmail(db: Session, email: str) -> NguoiDung | None:
    return db.query(NguoiDung).filter(NguoiDung.email == email).first()


def getById(db: Session, maNguoiDung: int) -> NguoiDung | None:
    return db.query(NguoiDung).filter(NguoiDung.maNguoiDung == maNguoiDung).first()


def create(db: Session, hoTen: str, email: str, matKhauHash: str, vaiTro: str) -> NguoiDung:
    nguoiDung = NguoiDung(hoTen=hoTen, email=email, matKhau=matKhauHash, vaiTro=vaiTro)
    db.add(nguoiDung)
    db.commit()
    db.refresh(nguoiDung)
    return nguoiDung


def updateMatKhau(db: Session, nguoiDung: NguoiDung, matKhauHashMoi: str) -> NguoiDung:
    nguoiDung.matKhau = matKhauHashMoi
    db.commit()
    db.refresh(nguoiDung)
    return nguoiDung
