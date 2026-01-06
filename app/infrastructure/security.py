import datetime

from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, timezone, datetime
import hashlib
import secrets


def get_expire_refresh_date(date):
    now = datetime.now(timezone.utc)
    expire_date = (now + timedelta(days=date))
    return expire_date


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh(token: str):
    return hashlib.sha256(token.encode("utf8")).hexdigest()


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_token(sub: str, secret_key: str, expire_date: int, algorithm: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": now.timestamp(),
        "expire": (now + timedelta(minutes=expire_date)).timestamp()
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
