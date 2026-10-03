from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class Buku(Base):
    __tablename__ = "buku"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    judul: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    penulis: Mapped[str] = mapped_column(String(255), index=True)
    tahun: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(30))
    qty: Mapped[int] = mapped_column(Integer, default=0)
    tersedia: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    created_by: Mapped[str] = mapped_column(String(50))
    modify_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    modify_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

