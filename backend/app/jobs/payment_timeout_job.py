"""
Background job (Cronjob) xu ly timeout thanh toan (TC35).
Don 'Cho thanh toan' co ma QR da qua han ma chua nhan duoc webhook thanh cong
se tu dong duoc chuyen thanh 'Da huy', ma QR cu bi vo hieu hoa (chuyen HET_HAN).
"""
import asyncio
import logging
from datetime import datetime, timezone

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.enums import TrangThaiDonHang, TrangThaiThanhToan
from app.repositories import don_hang_repository, thanh_toan_repository

logger = logging.getLogger("payment_timeout_job")


def quetDonHetHanMotLan():
    """Thuc thi 1 lan quet: tim tat ca don 'Cho thanh toan' co thanh toan qua han."""
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        donHangs = don_hang_repository.getPendingExpired(db, now, TrangThaiDonHang.CHO_THANH_TOAN)
        soDonBiHuy = 0
        for donHang in donHangs:
            thanhToan = donHang.thanhToan
            if not thanhToan or thanhToan.trangThai != TrangThaiThanhToan.CHO_XU_LY:
                continue

            thoiHan = thanhToan.thoiHanThanhToan
            if thoiHan.tzinfo is None:
                thoiHan = thoiHan.replace(tzinfo=timezone.utc)

            if now > thoiHan:
                thanh_toan_repository.updateTrangThai(db, thanhToan, TrangThaiThanhToan.HET_HAN)
                don_hang_repository.updateTrangThai(db, donHang, TrangThaiDonHang.DA_HUY)
                soDonBiHuy += 1

        if soDonBiHuy:
            logger.info("Da tu dong huy %s don hang qua han thanh toan", soDonBiHuy)
        return soDonBiHuy
    finally:
        db.close()


async def vongLapKiemTraTimeout():
    """Vong lap chay ngam song song voi ung dung, quet dinh ky theo cau hinh."""
    while True:
        try:
            quetDonHetHanMotLan()
        except Exception:  # khong de loi cua 1 lan quet lam chet ca vong lap
            logger.exception("Loi khi quet don hang het han thanh toan")
        await asyncio.sleep(settings.PAYMENT_TIMEOUT_CHECK_INTERVAL_SECONDS)
