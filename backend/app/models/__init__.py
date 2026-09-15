"""
Import tat ca model de SQLAlchemy Base.metadata biet duoc toan bo bang
khi goi Base.metadata.create_all(engine).
"""
from app.models.nguoi_dung import NguoiDung  # noqa: F401
from app.models.mon_an import MonAn  # noqa: F401
from app.models.don_hang import DonHang  # noqa: F401
from app.models.chi_tiet_don_hang import ChiTietDonHang  # noqa: F401
from app.models.thanh_toan import ThanhToan  # noqa: F401
from app.models.danh_gia import DanhGia  # noqa: F401
