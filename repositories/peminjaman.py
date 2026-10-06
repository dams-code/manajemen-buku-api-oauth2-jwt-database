from schemas.peminjaman import HPeminjamanResponse
from datetime import datetime
from schemas.peminjaman import *
from models.peminjaman import *
from models.buku import Buku
from helpers.generate_no_pinjam import generate_no_pinjam
from core.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException

async def result_add_Hpinjam(hpeminjaman: HPeminjamanCreate, username_aktif: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultHpeminjaman[HPeminjamanResponse]:
    
    if not hpeminjaman.details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="List Buku yang dipinjam tidak boleh kosong"
        )

    try:
        generate_no_pinjam = await generate_no_pinjam(sesi_db)

        total_qty = sum(item.qty for item in hpeminjaman.details)

        result_header_pinjam = hpeminjaman(
            member_id=hpeminjaman.member_id,
            no_pinjam = hpeminjaman.no_pinjam,
            qty_pinjam = total_qty,
            tanggal_pinjam = hpeminjaman.tanggal_pinjam,
            tanggal_kembali = hpeminjaman.tanggal_kembali,
            status = "terbuat",

            created_at = hpeminjaman.created_at,
            created_by = hpeminjaman.created_by
        )

        sesi_db.add(result_header_pinjam)

        await sesi_db.flush()

        for item in hpeminjaman.details:
            buku = await sesi_db.get(Buku, item.buku_id)

            if not buku:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail=f"Buku id {item.buku_id} tidak ditemukan"
                )
            
            if buku.qty < item.qty:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail=f"Stok buku {buku.judul} tidak mencukupi, stok tinggal {buku.qty}"
                )

            buku.qty = item.qty

            result_detail_pinjam = DPeminjamanCreate()




    except HTTPException:
        await sesi_db.rollback()
        raise
    except Exception as e:
        await sesi_db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan : {str(e)}"
        )
    

    generate_no_pinjam = await generate_no_pinjam(get_database);

    dataHeaderPinjam = hpeminjaman.model_dump(exclude_unset=True)

    result_header_pinjam = HPeminjamanCreate(
        **dataHeaderPinjam,
        no_pinjam=generate_no_pinjam,
        created_at = datetime.now(),
        created_by= username_aktif
    )

    sesi_db.add(result_header_pinjam)

    await sesi_db.commit()
    await sesi_db.refresh(result_header_pinjam)

    return ResultHpeminjaman[HPeminjamanResponse](
        status=status.HTTP_201_CREATED,
        pesan=f"Header Peminjaman buku berhasil terbuat",
        data=HPeminjamanResponse.model_validate(result_header_pinjam)
    )

