from fastapi import Depends, HTTPException, status
from models.peminjaman import *
from core.database import get_database
from schemas.peminjaman import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

async def result_pembatalan_buku(id: int, no_pinjam: str, username_aktif: str, sesi_db: AsyncSession = Depends(get_database))-> ResultHpeminjaman[HPeminjamanResponse]:

    query = select(HPeminjaman).where(and_(HPeminjaman.id == id, HPeminjaman.no_pinjam == no_pinjam))

    result = await sesi_db.execute(query)

    result_pembatalan = result.scalars().first()

    if not result_pembatalan:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Data Peminjaman buku, Id {id} dengan No Pinjam {no_pinjam} tidak ditemukan"
        )

    for detail in result_pembatalan.details:
        if detail.buku:
            detail.buku.qty += detail.qty

    result_pembatalan.status = StatusPinjam.BATAL
    result_pembatalan.modify_at = datetime.now()
    result_pembatalan.modify_by = username_aktif

    await sesi_db.commit()
    await sesi_db.refresh(result_pembatalan)

    return ResultHpeminjaman[HPeminjamanResponse](
        status=status.HTTP_200_OK,
        pesan=f"Proses pembatalan buku dengan No Pinjam {no_pinjam} berhasil",
        data=HPeminjamanResponse.model_validate(result_pembatalan)
    )


async def result_get_pembatalan_buku(no_pinjam: str, nama_member: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultHpeminjaman[list[HPeminjamanResponseNonDetail]]:

    query = select(HPeminjaman).where(HPeminjaman.status == StatusPinjam.BATAL)

    conditions = []

    if no_pinjam is not None:
        conditions.append(HPeminjaman.no_pinjam.ilike(f"%{no_pinjam}%"))

    if nama_member is not None:
        conditions.append(HPeminjaman.nama_member.ilike(f"%{nama_member}%"))

    if conditions:
        query = query.where(or_(*conditions))

    result = await sesi_db.execute(query)

    result_get_pembatalan = result.scalars().all()

    if result_get_pembatalan is None or len(result_get_pembatalan) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar Pembatalan buku tidak ditemukan"
        )

    pesan = ""

    result_final = [HPeminjamanResponseNonDetail.model_validate(pembatalan) for pembatalan in result_get_pembatalan]

    if no_pinjam is not None:
        pesan = f"Pembatalan buku dengan No Pinjam {no_pinjam} ditemukan"
    elif nama_member is not None:
        pesan = f"Pembatalan buku dengan nama member awalan {nama_member} ditemukan"
    else:
        pesan = f"List Pembatalan buku berhasil terload (total {len(result_get_pembatalan)} buku)"

    return ResultHpeminjaman[list[HPeminjamanResponseNonDetail]](
        status=status.HTTP_200_OK,
        pesan=pesan,
        data=result_final
    )
        

