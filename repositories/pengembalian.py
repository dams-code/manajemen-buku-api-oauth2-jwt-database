

from schemas.peminjaman import ResultHpeminjaman, HPeminjamanResponse
from core.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from models.peminjaman import HPeminjaman
from sqlalchemy import select, and_
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




    




