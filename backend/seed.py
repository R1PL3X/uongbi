"""
Script chen du lieu mau (Seed Data) de Demo:
- 3 tai khoan: Admin / Staff (nhan vien Canteen) / Buyer (sinh vien).
- 10 mon an da dang trang thai (Con hang / Het hang / 1 mon da xoa mem de demo).
- 5 don hang lich su voi cac trang thai khac nhau de trang Dashboard Admin
  co so lieu hien thi bieu do (doanh thu, so don).

Chay: python seed.py   (chay tu thu muc backend/, sau khi da cai dat requirements.txt)
Luu y: script se XOA SACH va tao lai toan bo du lieu trong DB de dam bao demo sach.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.database import Base, engine, SessionLocal  # noqa: E402
from app.core.security import hashPassword  # noqa: E402
from app import models  # noqa: E402,F401
from app.models.nguoi_dung import NguoiDung  # noqa: E402
from app.models.mon_an import MonAn  # noqa: E402
from app.models.don_hang import DonHang  # noqa: E402
from app.models.chi_tiet_don_hang import ChiTietDonHang  # noqa: E402
from app.models.thanh_toan import ThanhToan  # noqa: E402
from app.models.enums import (  # noqa: E402
    VaiTro,
    TrangThaiMonAn,
    TrangThaiDonHang,
    TrangThaiThanhToan,
    PhuongThucThanhToan,
)


def seed():
    print("== Dang tao lai toan bo bang trong DB ==")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ---------- 3 tai khoan mau ----------
        admin = NguoiDung(
            hoTen="Nguyen Van Quan Ly",
            email="admin@uongbigo.vn",
            matKhau=hashPassword("Admin@123"),
            vaiTro=VaiTro.ROLE_ADMIN,
        )
        staff = NguoiDung(
            hoTen="Tran Thi Bep",
            email="staff@uongbigo.vn",
            matKhau=hashPassword("Staff@123"),
            vaiTro=VaiTro.ROLE_STAFF,
        )
        buyer = NguoiDung(
            hoTen="Le Van Sinh Vien",
            email="buyer@uongbigo.vn",
            matKhau=hashPassword("Buyer@123"),
            vaiTro=VaiTro.ROLE_BUYER,
        )
        db.add_all([admin, staff, buyer])
        db.commit()
        db.refresh(admin)
        db.refresh(staff)
        db.refresh(buyer)
        print(f"Da tao 3 tai khoan: {admin.email} / {staff.email} / {buyer.email}")

        # ---------- 10 mon an da dang trang thai ----------
        monAnData = [
            ("Com tam suon bi cha", 35000, "Com tam kieu Sai Gon, suon nuong, bi, cha trung", TrangThaiMonAn.CON_HANG),
            ("Bun bo Hue", 30000, "Bun bo cay dam da huong vi mien Trung", TrangThaiMonAn.CON_HANG),
            ("Pho bo tai", 32000, "Pho bo truyen thong, nuoc dung ham xuong 8 tieng", TrangThaiMonAn.CON_HANG),
            ("Banh mi op la", 20000, "Banh mi gion, trung op la, pate, rau thom", TrangThaiMonAn.CON_HANG),
            ("Xoi xeo", 15000, "Xoi xeo dau xanh, hanh phi thom bui", TrangThaiMonAn.CON_HANG),
            ("Mi xao bo", 28000, "Mi xao gion voi bo va rau cu", TrangThaiMonAn.CON_HANG),
            ("Com ga xoi mo", 33000, "Com ga xoi mo kieu Hai Nam", TrangThaiMonAn.HET_HANG),
            ("Bun cha Ha Noi", 35000, "Bun cha nuong than hoa dam vi Ha Noi", TrangThaiMonAn.HET_HANG),
            ("Chao long", 25000, "Chao long heo nong hoi, an kem que", TrangThaiMonAn.CON_HANG),
            ("Banh cuon", 22000, "Banh cuon nhan thit mong, cha lua, nuoc mam", TrangThaiMonAn.CON_HANG),
        ]
        monAns = []
        for tenMon, donGia, moTa, trangThai in monAnData:
            monAn = MonAn(tenMon=tenMon, donGia=donGia, moTa=moTa, trangThai=trangThai)
            db.add(monAn)
            monAns.append(monAn)
        db.commit()
        for m in monAns:
            db.refresh(m)

        # Them 1 mon da bi xoa mem de demo tinh nang Soft Delete (van con trong DB
        # nhung khong hien thi tren menu cong khai / man hinh Admin loc)
        monDaXoa = MonAn(
            tenMon="Mon dac biet (ngung ban)",
            donGia=40000,
            moTa="Mon nay da bi Admin xoa (soft delete) - van con du lieu de khong anh huong lich su don hang cu",
            trangThai=TrangThaiMonAn.DA_XOA,
        )
        db.add(monDaXoa)
        db.commit()
        db.refresh(monDaXoa)
        print(f"Da tao {len(monAns)} mon an + 1 mon da xoa mem (demo Soft Delete)")

        # ---------- 5 don hang lich su, da dang trang thai ----------
        now = datetime.now(timezone.utc)

        def taoDonHoanChinh(monChon, soLuongList, trangThaiDon, lechNgay, maDonRutGon=None):
            tongTien = sum(m.donGia * sl for m, sl in zip(monChon, soLuongList))
            donHang = DonHang(
                maNguoiDung=buyer.maNguoiDung,
                ngayDat=now - timedelta(days=lechNgay),
                tongTien=tongTien,
                trangThai=trangThaiDon,
                thoiGianNhan=(now - timedelta(days=lechNgay)).replace(hour=11, minute=30),
                maDonRutGon=maDonRutGon,
            )
            db.add(donHang)
            db.commit()
            db.refresh(donHang)

            for monAn, soLuong in zip(monChon, soLuongList):
                db.add(
                    ChiTietDonHang(
                        maDonHang=donHang.maDonHang,
                        maMon=monAn.maMon,
                        soLuong=soLuong,
                        donGia=monAn.donGia,
                        thanhTien=monAn.donGia * soLuong,
                    )
                )
            db.commit()

            if trangThaiDon != TrangThaiDonHang.CHO_THANH_TOAN:
                thanhToanTrangThai = {
                    TrangThaiDonHang.DA_HUY: TrangThaiThanhToan.HET_HAN,
                }.get(trangThaiDon, TrangThaiThanhToan.THANH_CONG)
                db.add(
                    ThanhToan(
                        maDonHang=donHang.maDonHang,
                        phuongThuc=PhuongThucThanhToan.VIETQR,
                        soTien=tongTien,
                        trangThai=thanhToanTrangThai,
                        maQr=f"seed-{donHang.maDonHang}",
                        thoiHanThanhToan=donHang.ngayDat + timedelta(minutes=5),
                        ngayThanhToan=donHang.ngayDat + timedelta(minutes=2)
                        if thanhToanTrangThai == TrangThaiThanhToan.THANH_CONG
                        else None,
                    )
                )
                db.commit()
            return donHang

        # 3 don da Hoan thanh (tinh vao doanh thu)
        taoDonHoanChinh([monAns[0], monAns[4]], [2, 1], TrangThaiDonHang.HOAN_THANH, 3, "#001")
        taoDonHoanChinh([monAns[1]], [1], TrangThaiDonHang.HOAN_THANH, 2, "#002")
        taoDonHoanChinh([monAns[2], monAns[3]], [1, 2], TrangThaiDonHang.HOAN_THANH, 1, "#003")
        # 1 don Da huy (KHONG tinh vao doanh thu - vi du timeout thanh toan)
        taoDonHoanChinh([monAns[5]], [1], TrangThaiDonHang.DA_HUY, 1)
        # 1 don dang Cho thanh toan (moi tao, chua thanh toan)
        taoDonHoanChinh([monAns[8], monAns[9]], [1, 1], TrangThaiDonHang.CHO_THANH_TOAN, 0)

        print("Da tao 5 don hang lich su (3 Hoan thanh, 1 Da huy, 1 Cho thanh toan)")

        print("\n== SEED DATA HOAN TAT ==")
        print("Tai khoan demo:")
        print("  Admin : admin@uongbigo.vn / Admin@123")
        print("  Staff : staff@uongbigo.vn / Staff@123")
        print("  Buyer : buyer@uongbigo.vn / Buyer@123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
