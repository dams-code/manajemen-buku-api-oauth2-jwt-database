

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.peminjaman import ResultDpeminjaman, HPeminjamanResponse
from schemas.roles import Roles
from typing import Annotated
from repositories.roles import CekRole
from core.database import get_database
from repositories.pengembalian import result_pengembalian_buku

router_pengembalian = APIRouter(prefix="/pengembalian", tags=["Pengembalian"])

@router_pengembalian.put("/{id}", response_model=ResultDpeminjaman[HPeminjamanResponse])
async def pengembalian_buku(id: int, no_pinjam: Annotated[str, Query(max_length=14)], username_aktif: str = Depends(CekRole([Roles.ADMIN])), sesi_db: AsyncSession = Depends(get_database)):
    return await result_pengembalian_buku(id, no_pinjam, username_aktif, sesi_db)
