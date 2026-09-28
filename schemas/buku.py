from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BukuBase(BaseModel):
    id: int
    judul: str
    penulis: str
    tahun: int
    genre: str
    tersedia: bool = True
    qty: int | None = 0
    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str | None

    model_config = ConfigDict(from_attributes=True)

class BukuCreate(BaseModel):
    judul: str
    penulis: str
    tahun: int
    qty: int
    genre: str
    tersedia: bool = True
    qty: int | None = 0

class BukuUpdate(BaseModel):
    judul: str | None
    penulis: str | None
    tahun: int | None
    qty: int | None
    genre: str | None
    tersedia: bool | None
    qty: int | None

# class Buku(BaseModel):
#     judul: str
#     penulis: str
#     tahun: int
#     genre: str
#     tersedia: bool
    
class ResultBuku(BaseModel, Generic[T]):
    status: int
    pesan: str
    data: Optional[T] = None