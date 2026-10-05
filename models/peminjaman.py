from alembic.autogenerate.compare import server_defaults
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, func, DateTime, ForeignKey, Enum as sqlEnum
from typing import Optional, List

import enum

class TimestampPeminjaman:
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String(50), nullable=False)

    modify_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    modify_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

class StatusPinjam(str, enum.Enum):
    TERBUAT = "terbuat"
    KEMBALI = "kembali"
    BATAL = "batal"

class HPeminjaman(Base, TimestampPeminjaman):

    __tablename__ = "hpeminjaman"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    no_pinjam: Mapped[str] = mapped_column(String(14), index=True, unique=True)
    qty_pinjam: Mapped[int] = mapped_column(Integer)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    status: Mapped[StatusPinjam] = mapped_column(
        sqlEnum(StatusPinjam, native_enum=False),
        default=StatusPinjam.TERBUAT,
        nullable=False
    )
    tanggal_pinjam: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    tanggal_kembali: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    details: Mapped[List["DPeminjaman"]] = relationship(
        "DPeminjaman",
        back_populates="header",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

class DPeminjaman(Base, TimestampPeminjaman):

    __tablename__ = "dpeminjaman"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    header_id: Mapped[int] = mapped_column(ForeignKey("hpeminjaman.id"))
    buku_id: Mapped[int] = mapped_column(ForeignKey("buku.id"))

    header: Mapped["HPeminjaman"] = relationship("HPeminjaman", back_populates="details")
