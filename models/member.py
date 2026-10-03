from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

from typing import Optional

class Member(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nama: Mapped[str] = mapped_column(String(255), index=True)
    alamat: Mapped[str] = mapped_column(String(255))
    no_telp: Mapped[str] = mapped_column(String(15), unique=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    created_by: Mapped[str] = mapped_column(String(50))
    modify_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    modify_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    