"""Security utility functions."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify plain text password using hashed password."""
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    """Hash plain text password."""
    return pwd_context.hash(password)
