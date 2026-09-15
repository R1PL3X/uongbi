"""
Presentation Layer - API endpoints cho Admin Dashboard (Sprint 4 - Epic 1).
TC60 - Phan quyen tuyet doi: chi ROLE_ADMIN duoc truy cap, moi tai khoan khac
bi tu choi voi HTTP 403 Forbidden (dam bao boi dependency requireRoles).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.deps import requireRoles
from app.models.enums import VaiTro
from app.models.nguoi_dung import NguoiDung
from app.schemas.mon_an import MonAnResponse, MonAnCreateRequest, MonAnUpdateRequest
from app.schemas.don_hang import DonHangResponse
from app.schemas.thong_ke import ThongKeResponse
from app.services import mon_an_service, don_hang_service, thong_ke_service
from app.repositories import don_hang_repository

router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(requireRoles(VaiTro.ROLE_ADMIN))])


# ---------- US17/US18 - Quan ly Menu (CRUD, TC54-TC57) ----------

@router.get("/mon-an", response_model=list[MonAnResponse])
def danhSachMonAdmin(db: Session = Depends(getDb)):
    return mon_an_service.danhSachMenuAdmin(db)


@router.post("/mon-an", response_model=MonAnResponse, status_code=201)
def taoMonAn(payload: MonAnCreateRequest, db: Session = Depends(getDb)):
    """TC54 - Tao moi mon an (Ten, Anh, Gia, Mo ta)."""
    return mon_an_service.taoMonMoi(db, payload.tenMon, payload.donGia, payload.moTa, payload.hinhAnh)


@router.put("/mon-an/{maMon}", response_model=MonAnResponse)
def capNhatMonAn(maMon: int, payload: MonAnUpdateRequest, db: Session = Depends(getDb)):
    """TC55 - Cap nhat gia va trang thai Con/Het hang."""
    return mon_an_service.capNhatMon(
        db, maMon, payload.tenMon, payload.donGia, payload.moTa, payload.hinhAnh, payload.trangThai
    )


@router.delete("/mon-an/{maMon}", response_model=MonAnResponse)
def xoaMonAn(maMon: int, db: Session = Depends(getDb)):
    """TC56 - Xoa mem (Soft Delete): chi an mon khoi menu, khong xoa cung khoi DB."""
    return mon_an_service.xoaMon(db, maMon)


# ---------- US19 - Lich su don hang ----------

@router.get("/don-hang", response_model=list[DonHangResponse])
def lichSuDonHang(db: Session = Depends(getDb)):
    return don_hang_repository.getAll(db)


# ---------- US20 - Thong ke doanh thu/don hang (TC59) ----------

@router.get("/thong-ke", response_model=ThongKeResponse)
def thongKe(db: Session = Depends(getDb)):
    return thong_ke_service.layThongKe(db)
