"""
Presentation Layer - Pydantic Schemas cho thong ke Admin Dashboard.
"""
from pydantic import BaseModel


class ThongKeResponse(BaseModel):
    tongSoDonHoanThanh: int
    tongSoDonTatCa: int
    tongDoanhThu: float
    soMonDangBan: int
    soMonHetHang: int
