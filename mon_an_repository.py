"""
Data Access Layer - Repository cho MonAn.
"""
from sqlalchemy.orm import Session

from app.models.mon_an import MonAn
from app.models.enums import TrangThaiMonAn


def getAllVisible(db: Session) -> list[MonAn]:
    """Lay danh sach mon an hien thi cho khach (khong bao gom mon da xoa mem)."""
    return (
        db.query(MonAn)
        .filter(MonAn.trangThai != TrangThaiMonAn.DA_XOA)
        .order_by(MonAn.maMon.asc())
        .all()
    )


def getAllForAdmin(db: Session) -> list[MonAn]:
    """Admin xem toan bo, bao gom ca mon da an (da xoa mem) de doi soat neu can."""
    return db.query(MonAn).order_by(MonAn.maMon.asc()).all()


def getById(db: Session, maMon: int) -> MonAn | None:
    return db.query(MonAn).filter(MonAn.maMon == maMon).first()


def create(db: Session, tenMon: str, donGia: float, moTa: str | None, hinhAnh: str | None) -> MonAn:
    monAn = MonAn(
        tenMon=tenMon,
        donGia=donGia,
        moTa=moTa,
        hinhAnh=hinhAnh,
        trangThai=TrangThaiMonAn.CON_HANG,
    )
    db.add(monAn)
    db.commit()
    db.refresh(monAn)
    return monAn


def update(db: Session, monAn: MonAn, **fields) -> MonAn:
    for key, value in fields.items():
        if value is not None:
            setattr(monAn, key, value)
    db.commit()
    db.refresh(monAn)
    return monAn


def softDelete(db: Session, monAn: MonAn) -> MonAn:
    """Xoa mem: chi doi trangThai sang DA_XOA, khong xoa ban ghi khoi DB
    de khong lam anh huong lich su Don Hang cu da tham chieu toi mon nay."""
    monAn.trangThai = TrangThaiMonAn.DA_XOA
    db.commit()
    db.refresh(monAn)
    return monAn
