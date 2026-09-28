from schemas.buku import *
from core.database import get_database
from schemas.user import UserBase
from schemas.roles import Roles
from fastapi import APIRouter, Query, Path, Depends
from repositories.buku import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from repositories.roles import CekRole

from sqlalchemy.ext.asyncio import AsyncSession

router_buku = APIRouter(prefix="/buku", tags=["buku"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router_buku.get("", response_model=ResultBuku[BukuBase | list[BukuBase]], dependencies=[Depends(CekRole([Roles.ADMIN, Roles.MANAJER]))])
# async def get_buku(id: Annotated[int | None, Query()] = None, judul: Annotated[str | None, Query()] = None, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def get_buku(id: Annotated[int | None, Query()] = None, judul: Annotated[str | None, Query()] = None, sesi_db: AsyncSession = Depends(get_database)):
    
    return await result_get_buku(id=id, judul=judul, sesi_db=sesi_db)

@router_buku.get("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN, Roles.MANAJER]))])
# async def get_buku_id(id: Annotated[int, Path(description="Cari Id Buku", gt=0)], token: Annotated[str, Depends(oauth2_scheme)] = None):
async def get_buku_id(id: Annotated[int, Path(description="Cari Id Buku", gt=0)], sesi_db: AsyncSession = Depends(get_database)):
    
    return await result_get_buku_id(id=id, sesi_db=sesi_db)

@router_buku.post("", response_model=ResultBuku[BukuBase], status_code=status.HTTP_201_CREATED)
# @router_buku.post("", response_model=ResultBuku[BukuBase], status_code=status.HTTP_201_CREATED, dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def add_buku(buku: Buku, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def add_buku(buku: BukuCreate ,user_aktif: UserBase = Depends(CekRole([Roles.ADMIN])), sesi_db: AsyncSession = Depends(get_database)):
    
    return await result_add_buku(buku=buku, user_aktif=user_aktif.username, sesi_db=sesi_db)

@router_buku.put("/{id}", response_model=ResultBuku[BukuBase])
# @router_buku.put("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def update_buku(id: Annotated[int, Path(description="Update Id Buku", gt=0)], buku: Buku, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def update_buku(id: Annotated[int, Path(description="Update Id Buku", gt=0)], buku: BukuUpdate, user_aktif: UserBase = Depends(CekRole([Roles.ADMIN])), sesi_db: AsyncSession = Depends(get_database)):
    
    return await result_update_buku(id, buku, user_aktif, sesi_db)

@router_buku.delete("/{id}", response_model=ResultBuku[None], dependencies=[Depends(CekRole([Roles.ADMIN]))])
async def delete_buku(id: Annotated[int, Path(description="Hapus Id Buku", gt=0)], sesi_db: AsyncSession = Depends(get_database)):
# async def delete_buku(id: Annotated[int, Path(description="Hapus Id Buku", gt=0)], token: Annotated[str, Depends(oauth2_scheme)] = None):
    
    return await result_delete_buku(id=id, sesi_db=sesi_db)

@router_buku.patch("/{id}", response_model=ResultBuku[BukuBase])
# @router_buku.patch("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def update_status_buku(id: Annotated[int, Path(description="Update Status Buku", gt=0)], tersedia: Annotated[bool, Query(description="Ketersedian buku (true/false)")], token: Annotated[str, Depends(oauth2_scheme)] = None):
async def update_status_buku(id: Annotated[int, Path(description="Update Status Buku", gt=0)], tersedia: Annotated[bool, Query(description="Ketersedian buku (true/false)")], user_aktif: UserBase = Depends(CekRole([Roles.ADMIN])) ,sesi_db: AsyncSession = Depends(get_database)):
    
    return await result_update_status_buku(id=id, tersedia=tersedia, user_aktif=user_aktif, sesi_db=sesi_db)
