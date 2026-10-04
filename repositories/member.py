from models.member import Member
from schemas.member import *

from core.database import get_database
from sqlalchemy import select, update, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status


async def result_get_member(id: int | None, nama: str | None, sesi_db: AsyncSession) -> ResultMember[list[MemberBase]]:

    query = select(Member)

    conditions = []

    if id is not None:
        conditions.append(Member.id == id)

    if nama is not None:
        conditions.append(Member.nama.ilike(f"%{nama}%"))

    if conditions:
        query = query.where(or_(*conditions))

    result = await sesi_db.execute(query)

    result_data_member = result.scalars().all()

    if result_data_member is None or len(result_data_member) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data member tidak ditemukan"
        )

    data_member = [MemberBase.model_validate(member) for member in result_data_member];

    if id is not None:
        pesan=f"Member id {id} ditemukan"
    elif nama is not None:
        pesan=f"Member dengan awalan nama {nama} ditemukan, total {len(nama)} data"
    else:
        pesan=f"List data member berhasil terload (total {len(result_data_member)} member)"

    return ResultMember[list[MemberBase]](
        status=status.HTTP_200_OK,
        pesan=pesan,
        data=data_member
    )


async def result_add_member(member: BuatMember, username_aktif: str, sesi_db: AsyncSession = Depends(get_database)):

    query = select(Member).where(Member.nama == member.nama)

    result = await sesi_db.execute(query)

    cek_member = result.scalar_one_or_none()

    if cek_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member dengan nama {member.nama} sudah terdaftar"
        )

    data_member = member.model_dump(exclude_unset=True)

    result_data_member = Member(
        **data_member,
        created_at = datetime.now(),
        created_by = username_aktif
    )

    sesi_db.add(result_data_member)

    await sesi_db.commit()

    await sesi_db.refresh(result_data_member)

    return ResultMember[MemberBase](
        status=status.HTTP_200_OK,
        pesan=f"Member {member.nama} berhasil ditambahkan",
        data=MemberBase.model_validate(result_data_member)
    )

async def result_get_member_id(id: int, sesi_db: AsyncSession = Depends(get_database)) -> ResultMember[MemberBase]:

    query = select(Member).where(Member.id == id)

    result = await sesi_db.execute(query)

    result_data_member = result.scalar_one_or_none()

    if result_data_member is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Data member tidak ditemukan"
        )

    return ResultMember[MemberBase](
        status=status.HTTP_200_OK,
        pesan="Member ditemukan",
        data = MemberBase.model_validate(result_data_member)
    )

async def result_update_member(id: int, member: UpdateMember, username_aktif: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultMember[MemberBase]:

    query = select(Member).where(Member.id == id)

    result = await sesi_db.execute(query)

    result_data_member = result.scalar_one_or_none()

    if result_data_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member dengan id {id} tidak ditemukan"
        )

    data_member = member.model_dump(exclude_unset=True)

    for key, item in data_member.items():
        setattr(result_data_member, key, item)

    result_data_member.modify_at = datetime.now()
    result_data_member.modify_by = username_aktif

    await sesi_db.commit()
    await sesi_db.refresh(result_data_member)

    return ResultMember[MemberBase](
        status=status.HTTP_200_OK,
        pesan=f"Member dengan id {id} berhasil diupdate",
        data=MemberBase.model_validate(result_data_member)
    )

async def result_delete_member(id: int, sesi_db: AsyncSession = Depends(get_database)) -> ResultMember[None]:

    query = select(Member).where(Member.id == id)

    result = await sesi_db.execute(query)

    result_data_member = result.scalar_one_or_none()

    if result_data_member is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Member id {id} tidak ditemukan"
        )

    await sesi_db.delete(result_data_member)

    await sesi_db.commit()

    return ResultMember[None](
        status=status.HTTP_200_OK,
        pesan=f"Member id {id} berhasil dihapus",
        data=None
    )

async def result_update_status_member(id: int, status_member: bool, username_aktif: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultMember[MemberBase]:

    query = select(Member).where(Member.id == id)

    result = await sesi_db.execute(query)

    result_data_member = result.scalar_one_or_none()

    if result_data_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member dengan id {id} tidak ditemukan"
        )

    result_data_member.status = status_member
    result_data_member.modify_at = datetime.now()
    result_data_member.modify_by = username_aktif

    await sesi_db.commit()
    await sesi_db.refresh(result_data_member)

    return ResultMember[MemberBase](
        status=status.HTTP_200_OK,
        pesan=f"Status member dengan id {id} berhasil diupdate",
        data=MemberBase.model_validate(result_data_member)
    )