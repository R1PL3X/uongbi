"""
Cac Dependency dung chung cho Presentation Layer:
- getCurrentUser: giai ma JWT tu header Authorization, tra ve NguoiDung dang dang nhap.
- requireRoles: factory tao dependency kiem tra RBAC, tra 403 Forbidden neu sai quyen (TC60).
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import getDb
from app.core.security import decodeAccessToken
from app.models.nguoi_dung import NguoiDung
from app.repositories import nguoi_dung_repository

# Chi dung de sinh UI "Authorize" tren Swagger (/api/docs); token thuc su
# duoc client tu quan ly va gui qua header Authorization: Bearer <token>.
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def getCurrentUser(
    token: str | None = Depends(oauth2Scheme),
    db: Session = Depends(getDb),
) -> NguoiDung:
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Khong the xac thuc thong tin dang nhap",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentialsException

    payload = decodeAccessToken(token)
    if payload is None:
        raise credentialsException

    maNguoiDung = payload.get("sub")
    if maNguoiDung is None:
        raise credentialsException

    nguoiDung = nguoi_dung_repository.getById(db, int(maNguoiDung))
    if nguoiDung is None:
        raise credentialsException

    return nguoiDung


def requireRoles(*allowedRoles: str):
    """
    Factory tra ve dependency chi cho phep cac Role duoc liet ke.
    Bat ky tai khoan nao khac co gang truy cap deu bi tu choi voi HTTP 403 (TC60).
    """

    def _checkRole(currentUser: NguoiDung = Depends(getCurrentUser)) -> NguoiDung:
        if currentUser.vaiTro not in allowedRoles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tai khoan vai tro '{currentUser.vaiTro}' khong co quyen truy cap chuc nang nay",
            )
        return currentUser

    return _checkRole
