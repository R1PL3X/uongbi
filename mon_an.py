"""
Presentation Layer - Pydantic Schemas cho MonAn.
"""
from pydantic import BaseModel, Field


class MonAnCreateRequest(BaseModel):
    tenMon: str = Field(..., min_length=1, max_length=150)
    donGia: float = Field(..., gt=0)
    moTa: str | None = None
    hinhAnh: str | None = None


class MonAnUpdateRequest(BaseModel):
    tenMon: str | None = None
    donGia: float | None = Field(default=None, gt=0)
    moTa: str | None = None
    hinhAnh: str | None = None
    trangThai: str | None = None  # CON_HANG | HET_HANG


class MonAnResponse(BaseModel):
    maMon: int
    tenMon: str
    donGia: float
    moTa: str | None = None
    hinhAnh: str | None = None
    trangThai: str

    class Config:
        from_attributes = True
