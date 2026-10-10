
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_database
from schemas.peminjaman import *
from schemas.roles import Roles
from repositories.roles import CekRole
from repositories.pembatalan import *
from fastapi import APIRouter, Depends, Query
from typing import Annotated

router_pembatalan = APIRouter(prefix="/pembatalan", tags=["Pembatalan"])

@router_pembatalan.put("/{id}", response_model=ResultHpeminjaman[HPeminjamanResponse])
async def pembatalan_buku(id: int, no_pinjam: Annotated[str, Query(max_length=14)], username_aktif: str = Depends(CekRole([Roles.ADMIN])), sesi_db: AsyncSession = Depends(get_database)):
    return await result_pembatalan_buku(id, no_pinjam, username_aktif, sesi_db)

@router_pembatalan.get("", response_model=ResultHpeminjaman[list[HPeminjamanResponseNonDetail]])
async def get_pembatalan_buku(no_pinjam: Annotated[str, Query(max_length=14)] = None, nama_member: Annotated[str, Query()] = None, sesi_db: AsyncSession = Depends(get_database)):
    return await result_get_pembatalan_buku(no_pinjam, nama_member, sesi_db)
