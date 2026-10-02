from datetime import datetime
from pydantic import BaseModel, ConfigDict

from typing import Generic, TypeVar, Optional

class MemberBase(BaseModel):
    id: int
    nama: str
    alamat: str
    no_telp: str
    status: bool
    created_at: datetime
    created_by: str
    modify_at: datetime | None = None
    modify_by: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BuatMember(BaseModel):
    nama: str
    alamat: str
    no_telp: str
    status: bool = True

    model_config = ConfigDict(from_attributes=True)

class UpdateMember(BaseModel):
    nama: str | None = None
    alamat: str | None = None
    no_telp: str | None = None

    model_config = ConfigDict(from_attributes=True)

T = TypeVar("T")

class ResultMember(BaseModel, Generic[T]):
    status: int
    pesan: str
    data: Optional[T] = None
