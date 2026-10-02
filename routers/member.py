from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_database
from helpers.security import CekRole, Roles
from schemas.member import ResultMember, MemberBase
from repositories.member import *

router_member = APIRouter(prefix="/member",tags=["member"])

@router_member.get("", response_model=ResultMember[MemberBase | list[MemberBase]], dependencies=[Depends(CekRole([Roles.ADMIN, Roles.MANAJER]))])
async def get_member(id: int | None=None, nama: str | None=None, sesi_db: AsyncSession = Depends(get_database)):

    return await result_get_member(id, nama, sesi_db)

@router_member.post("", response_model=ResultMember[MemberBase])
async def add_member(member: BuatMember, username_aktif: str = Depends(CekRole(Roles.ADMIN)), sesi_db: AsyncSession = Depends(get_database)):

    return await result_add_member(member, username_aktif, sesi_db)
