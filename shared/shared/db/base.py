"""SQLAlchemy declarative base — imported by every module model."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
