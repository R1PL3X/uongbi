"""
Presentation Layer - API endpoints cho Auth (Sprint 1 - Epic 1).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.schemas.auth import (
    DangKyRequest,
    DangNhapRequest,
    QuenMatKhauRequest,
    QuenMatKhauResponse,
    TokenResponse,
    NguoiDungResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=NguoiDungResponse, status_code=201)
def dangKy(payload: DangKyRequest, db: Session = Depends(getDb)):
    """US01 - Dang ky tai khoan moi (email khong duoc trung lap)."""
    nguoiDung = auth_service.dangKy(db, payload.hoTen, payload.email, payload.matKhau, payload.vaiTro)
    return nguoiDung


@router.post("/login", response_model=TokenResponse)
def dangNhap(payload: DangNhapRequest, db: Session = Depends(getDb)):
    """US01 - Dang nhap, cap JWT va dieu huong theo Role (ROLE_BUYER/ROLE_STAFF/ROLE_ADMIN)."""
    accessToken, nguoiDung, redirectTo = auth_service.dangNhap(db, payload.email, payload.matKhau)
    return TokenResponse(
        accessToken=accessToken,
        nguoiDung=NguoiDungResponse.model_validate(nguoiDung),
        redirectTo=redirectTo,
    )


@router.post("/forgot-password", response_model=QuenMatKhauResponse)
def quenMatKhau(payload: QuenMatKhauRequest, db: Session = Depends(getDb)):
    """US02 - Khoi phuc mat khau khi quen."""
    message, matKhauTamThoi = auth_service.quenMatKhau(db, payload.email)
    return QuenMatKhauResponse(message=message, matKhauTamThoi=matKhauTamThoi)
