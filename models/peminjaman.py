from __future__ import annotations

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, func, DateTime, ForeignKey, Enum as sqlEnum
from typing import TYPE_CHECKING, Optional, List

from models.buku import Buku

import enum

if TYPE_CHECKING:
    from models.member import Member

class TimestampPeminjaman:
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String(50), nullable=False)

    modify_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    modify_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

class StatusPinjam(str, enum.Enum):
    TERBUAT = "terbuat"
    KEMBALI = "kembali"
    DIPINJAM = "dipinjam"
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

    member_ref: Mapped["Member"] = relationship("Member", back_populates="hpeminjaman_ref", lazy="joined")

class DPeminjaman(Base, TimestampPeminjaman):

    __tablename__ = "dpeminjaman"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    header_id: Mapped[int] = mapped_column(ForeignKey("hpeminjaman.id"))
    buku_id: Mapped[int] = mapped_column(ForeignKey("buku.id"))
    qty: Mapped[int] = mapped_column(Integer)

    header: Mapped["HPeminjaman"] = relationship("HPeminjaman", back_populates="details")
    buku: Mapped["Buku"] = relationship("Buku", lazy="joined")

    @property
    def judul(self) -> str | None:
        return self.buku.judul if self.buku else None
    
    @property
    def penulis(self) -> str | None:
        return self.buku.penulis if self.buku else None

    @property
    def genre(self) -> str | None:
        return self.buku.genre if self.buku else None
