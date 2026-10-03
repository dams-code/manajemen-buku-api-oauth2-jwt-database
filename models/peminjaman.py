from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, func, DateTime, ForeignKey
from typing import Optional, List

class HPeminjaman(Base):

    __tablename__ = "hpeminjaman"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    no_pinjam: Mapped[str] = mapped_column(String(7), index=True, unique=True)
    qty_pinjam: Mapped[int] = mapped_column(Integer)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    tanggal_pinjam: Mapped[DateTime] = mapped_column(DateTime, server_defaults=func.now())
    tanggal_kembali: Mapped[Optional[DateTime | None]] = mapped_column(DateTime, nullable=True)
    details: Mapped[List["DPeminjaman"]] = relationship(
        "DPeminjaman",
        back_populates="header",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

class DPeminjaman(Base):

    __tablename__ = "dpeminjaman"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    header_id: Mapped[int] = mapped_column(ForeignKey("hpeminjaman.id"))
    buku_id: Mapped[int] = mapped_column(ForeignKey("buku.id"))

    header: Mapped["HPeminjaman"] = relationship("HPeminjaman", back_populates="details")
