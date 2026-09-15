"""
Cac hang so (constants) dung chung: Role, trang thai Mon An, trang thai Don Hang,
trang thai Thanh Toan. Ten hang so viet HOA, phan cach bang dau gach duoi
(UPPER_SNAKE_CASE) theo dung quy uoc coding cua du an.
"""


class VaiTro:
    ROLE_BUYER = "ROLE_BUYER"      # Sinh vien / Nhan vien (nguoi mua)
    ROLE_STAFF = "ROLE_STAFF"      # Nhan vien Canteen / KDS
    ROLE_ADMIN = "ROLE_ADMIN"      # Quan ly Canteen

    ALL = (ROLE_BUYER, ROLE_STAFF, ROLE_ADMIN)


class TrangThaiMonAn:
    CON_HANG = "CON_HANG"
    HET_HANG = "HET_HANG"
    DA_XOA = "DA_XOA"  # Soft delete - khong xoa cung khoi DB


class TrangThaiDonHang:
    """
    State machine bat buoc, khong duoc nhay coc (TC41-TC45):
    CHO_THANH_TOAN -> DA_THANH_TOAN -> DANG_CHUAN_BI -> SAN_SANG_NHAN -> HOAN_THANH
    Nhanh re: CHO_THANH_TOAN -> DA_HUY (het han thanh toan / huy tay)
    """
    CHO_THANH_TOAN = "CHO_THANH_TOAN"
    DA_THANH_TOAN = "DA_THANH_TOAN"
    DANG_CHUAN_BI = "DANG_CHUAN_BI"
    SAN_SANG_NHAN = "SAN_SANG_NHAN"
    HOAN_THANH = "HOAN_THANH"
    DA_HUY = "DA_HUY"

    # Thu tu hop le cua state machine, dung de kiem tra buoc nhay tiep theo
    NEXT_STATE = {
        CHO_THANH_TOAN: {DA_THANH_TOAN, DA_HUY},
        DA_THANH_TOAN: {DANG_CHUAN_BI},
        DANG_CHUAN_BI: {SAN_SANG_NHAN},
        SAN_SANG_NHAN: {HOAN_THANH},
        HOAN_THANH: set(),
        DA_HUY: set(),
    }

    # Trang thai duoc tinh vao doanh thu thong ke
    TINH_DOANH_THU = {HOAN_THANH}


class TrangThaiThanhToan:
    CHO_XU_LY = "CHO_XU_LY"
    THANH_CONG = "THANH_CONG"
    THAT_BAI = "THAT_BAI"
    HET_HAN = "HET_HAN"


class PhuongThucThanhToan:
    VIETQR = "VIETQR"
    MOMO = "MOMO"
