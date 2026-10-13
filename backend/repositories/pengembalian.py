

from schemas.peminjaman import ResultHpeminjaman, HPeminjamanResponse, HPeminjamanResponseNonDetail
from core.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from models.peminjaman import HPeminjaman
from sqlalchemy import select, and_, or_
from models.peminjaman import StatusPinjam
from datetime import datetime

async def result_pengembalian_buku(id: int, no_pinjam: str, username_aktif: str, sesi_db: AsyncSession = Depends(get_database))-> ResultHpeminjaman[HPeminjamanResponse]:

    query = select(HPeminjaman).where(and_(HPeminjaman.id == id, HPeminjaman.no_pinjam == no_pinjam))

    result = await sesi_db.execute(query)

    result_data_pengembalian_buku = result.scalars().first()

    if not result_data_pengembalian_buku:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data Peminjaman buku, Id {id} dengan No Pinjam {no_pinjam} tidak ditemukan"
        )

    for detail in result_data_pengembalian_buku.details:
        if detail.buku:
            detail.buku.qty += detail.qty

    result_data_pengembalian_buku.status = StatusPinjam.KEMBALI
    result_data_pengembalian_buku.tanggal_kembali = datetime.now()
    result_data_pengembalian_buku.modify_at = datetime.now()
    result_data_pengembalian_buku.modify_by = username_aktif

    await sesi_db.commit()
    await sesi_db.refresh(result_data_pengembalian_buku)

    return ResultHpeminjaman[HPeminjamanResponse](
        status=status.HTTP_200_OK,
        pesan=f"Proses pengembalian buku dengan No Pinjam {no_pinjam} berhasil",
        data= HPeminjamanResponse.model_validate(result_data_pengembalian_buku)
    )

async def result_get_pengembalian_buku(no_pinjam: str, nama_member: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultHpeminjaman[list[HPeminjamanResponseNonDetail]]:

    query = select(HPeminjaman).where(HPeminjaman.status == StatusPinjam.KEMBALI)

    conditions = []

    if no_pinjam is not None:
        conditions.append(HPeminjaman.no_pinjam.ilike(f"%{no_pinjam}%"))
    
    if nama_member is not None:
        conditions.append(HPeminjaman.nama_member.ilike(f"%{nama_member}%"))

    if conditions:
        query = query.where(
            or_(*conditions)
        )
    
    result = await sesi_db.execute(query)

    result_get_pengembalian = result.scalars().all()

    if result_get_pengembalian is None or len(result_get_pengembalian) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar Pengembalian buku tidak ditemukan"
        )

    pesan = ""

    result_final = [HPeminjamanResponseNonDetail.model_validate(pengembalian) for pengembalian in result_get_pengembalian]

    if no_pinjam is not None:
        pesan = f"Peminjaman buku dengan No Pinjam {no_pinjam} ditemukan"
    elif nama_member is not None:
        pesan = f"Peminjaman buku dengan nama member awalan {nama_member} ditemukan"
    else:
        pesan = f"List peminjaman buku berhasil terload (total {len(result_get_pengembalian)} buku)"

    return ResultHpeminjaman[list[HPeminjamanResponseNonDetail]](
        status=status.HTTP_200_OK,
        pesan=pesan,
        data=result_final
    )







    




