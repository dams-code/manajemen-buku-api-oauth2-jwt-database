from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from core.database import get_database
from schemas.peminjaman import *
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.roles import Roles
from repositories.roles import CekRole
from repositories.peminjaman import *

router_peminjaman = APIRouter(prefix="/peminjaman", tags=["Peminjaman"])

@router_peminjaman.post("", response_model=ResultHpeminjaman[HPeminjamanResponse], status_code=status.HTTP_201_CREATED)
async def add_peminjaman(hpeminjaman: HPeminjamanCreate, username_aktif: str = Depends(CekRole([Roles.ADMIN])), sesi_db: AsyncSession = Depends(get_database)):

    return await result_add_Hpinjam(hpeminjaman, username_aktif, sesi_db)

@router_peminjaman.get("", dependencies=[Depends(CekRole([Roles.ADMIN]))], response_model=ResultHpeminjaman[list[HPeminjamanResponseNonDetail]])
async def get_hpeminjaman(no_member: Annotated[str, Query()]=None, sesi_db: AsyncSession = Depends(get_database)):
    return await result_get_hpeminjaman(no_member, sesi_db)

@router_peminjaman.get("/{id}", dependencies=[Depends(CekRole([Roles.ADMIN]))], response_model=ResultHpeminjaman[HPeminjamanResponse])
async def get_hpeminjaman_id(id: int, sesi_db: AsyncSession = Depends(get_database)):

    return await result_get_hpeminjaman_id(id, sesi_db)
