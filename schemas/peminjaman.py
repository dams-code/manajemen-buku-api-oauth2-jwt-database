from pydantic import BaseModel, ConfigDict
import datetime

from typing import List

class DPeminjamanCreate(BaseModel):
    buku_id: int

class DPeminjamanResponse(BaseModel):
    id: int
    header_id: int
    buku_id: int

    judul: str | None
    penulis: str | None
    genre: str | None

    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str | None

    model_config = ConfigDict(from_attributes=True)


class HPeminjamanCreate(BaseModel):
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
    details: List[DPeminjamanResponse]

    model_config = ConfigDict(from_attributes=True)


