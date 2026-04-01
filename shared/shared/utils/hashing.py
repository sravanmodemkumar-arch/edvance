"""Password hashing utilities — bcrypt cost 12."""
import os
from passlib.context import CryptContext

BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=BCRYPT_ROUNDS,
)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_otp(otp: str) -> str:
    return pwd_context.hash(otp)


def verify_otp(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
