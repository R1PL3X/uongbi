"""
Bao mat: bam mat khau (hash) va sinh/kiem tra JWT token.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Dung pbkdf2_sha256 de tranh phu thuoc build-native cua bcrypt tren moi moi truong,
# van la thuat toan bam mat khau an toan, khong luu plaintext.
pwdContext = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hashPassword(plainPassword: str) -> str:
    return pwdContext.hash(plainPassword)


def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    return pwdContext.verify(plainPassword, hashedPassword)


def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None) -> str:
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + (expiresDelta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
    toEncode.update({"exp": expire})
    return jwt.encode(toEncode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decodeAccessToken(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
