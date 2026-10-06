from typing import Annotated
from fastapi import APIRouter, Depends, status
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

