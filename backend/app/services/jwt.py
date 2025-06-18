"""JWT utility functions."""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import get_settings
from typing import Dict, Any


ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    """Create new access token."""
    settings = get_settings()

    to_encode = data.copy()
    expire = datetime.utcnow() \
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create new refresh token."""
    settings = get_settings()

    expire = datetime.utcnow() \
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> None | Dict[str, Any]:
    """Verify access token."""
    settings = get_settings()

    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
