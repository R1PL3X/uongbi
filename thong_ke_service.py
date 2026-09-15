"""
Business/Service Layer - logic thong ke doanh thu/don hang cho Admin Dashboard (US20).
"""
from sqlalchemy.orm import Session

from app.models.don_hang import DonHang
from app.models.mon_an import MonAn
from app.models.enums import TrangThaiDonHang, TrangThaiMonAn


def layThongKe(db: Session):
    """
    TC59 - Bao cao doanh thu chi tinh tong tien cua cac don hang co trang thai
    'Hoan thanh'. Khong cong don cac don 'Da huy' hoac 'Thanh toan that bai'.
    """
    tatCaDonHang = db.query(DonHang).all()
    donHoanThanh = [d for d in tatCaDonHang if d.trangThai in TrangThaiDonHang.TINH_DOANH_THU]

    tongDoanhThu = sum(d.tongTien for d in donHoanThanh)

    soMonDangBan = db.query(MonAn).filter(MonAn.trangThai == TrangThaiMonAn.CON_HANG).count()
    soMonHetHang = db.query(MonAn).filter(MonAn.trangThai == TrangThaiMonAn.HET_HANG).count()

    return {
        "tongSoDonHoanThanh": len(donHoanThanh),
        "tongSoDonTatCa": len(tatCaDonHang),
        "tongDoanhThu": tongDoanhThu,
        "soMonDangBan": soMonDangBan,
        "soMonHetHang": soMonHetHang,
    }
