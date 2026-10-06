from pydantic import BaseModel, ConfigDict
import datetime

from typing import List, Generic, TypeVar, Optional

T = TypeVar("T")

class DPeminjamanCreate(BaseModel):
    buku_id: int
    qty: int

class DPeminjamanResponse(BaseModel):
    id: int
    header_id: int
    buku_id: int
    qty: int

    judul: str | None
    penulis: str | None
    genre: str | None

    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str | None

    model_config = ConfigDict(from_attributes=True)

class ResultDpeminjaman(BaseModel, Generic[T]):
    status: int
    pesan: str
    data: Optional[T] = None

class HPeminjamanCreate(BaseModel):
    member_id: int
    qty_pinjam: int
    tanggal_pinjam: datetime
    tanggal_kembali: datetime | None
    status: str = "TERBUAT"

    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str | None

    details: List[DPeminjamanResponse]

    model_config = ConfigDict(from_attributes=True)

class HPeminjamanResponse(BaseModel):
    id: int
    member_id: int
    no_pinjam: str
    qty_pinjam: int
    tanggal_pinjam: datetime
    tanggal_kembali: datetime | None

    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str | None

    nama_member: str | None
    details = list[DPeminjamanResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ResultHpeminjaman(BaseModel, Generic[T]):
    status: int
    pesan: str
    data: Optional[T] = None

