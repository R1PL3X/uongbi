"""
Presentation Layer - Pydantic Schemas cho Auth (request/response cua API).
"""
from pydantic import BaseModel, EmailStr, Field


class DangKyRequest(BaseModel):
    hoTen: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    matKhau: str = Field(..., min_length=6, max_length=100)
    vaiTro: str = Field(default="ROLE_BUYER")


class DangNhapRequest(BaseModel):
    email: EmailStr
    matKhau: str


class QuenMatKhauRequest(BaseModel):
    email: EmailStr


class QuenMatKhauResponse(BaseModel):
    message: str
    # Demo/dev only: he thong chua tich hop gui email that su, nen tra ve
    # mat khau tam thoi truc tiep de test duoc luong. Production phai gui qua email.
    matKhauTamThoi: str | None = None


class NguoiDungResponse(BaseModel):
    maNguoiDung: int
    hoTen: str
    email: str
    vaiTro: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    nguoiDung: NguoiDungResponse
    redirectTo: str  # duong dan FE dieu huong theo Role
