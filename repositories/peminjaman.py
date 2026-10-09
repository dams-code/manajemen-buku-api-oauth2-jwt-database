from models.member import Member
from datetime import datetime
from schemas.peminjaman import *
from models.peminjaman import *
from models.buku import Buku
from helpers.generate_no_pinjam import generate_no_pinjam
from core.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from fastapi import Depends, status, HTTPException

async def result_get_hpeminjaman(no_pinjam: str, sesi_db: AsyncSession = Depends(get_database))-> ResultHpeminjaman[list[HPeminjamanResponseNonDetail]]:

    query = select(HPeminjaman).where(HPeminjaman.status == StatusPinjam.TERBUAT)

    if no_pinjam is not None:
        query = query.where(HPeminjaman.no_pinjam.ilike(f"%{no_pinjam}%"))

    result = await sesi_db.execute(query)

    list_peminjaman_buku = result.scalars().unique().all()

    if list_peminjaman_buku is None or len(list_peminjaman_buku) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="List peminjaman buku tidak ditemukan"
        )

    data_list_peminjaman_buku = [HPeminjamanResponseNonDetail.model_validate(list_peminjaman) for list_peminjaman in list_peminjaman_buku]

    pesan = ""

    if no_pinjam is not None:
        pesan = f"No Pinjam {no_pinjam} pada peminjaman buku tidak ditemukan"
    else:
        pesan += f"List peminjaman buku berhasil terload (total {len(list_peminjaman_buku)} buku)"

    return ResultHpeminjaman[list[HPeminjamanResponseNonDetail]](
        status=status.HTTP_200_OK,
        pesan=pesan,
        data=data_list_peminjaman_buku
    )

async def result_get_hpeminjaman_id(id: int, sesi_db: AsyncSession = Depends(get_database)):

    query = select(HPeminjaman).where(HPeminjaman.id == id)

    result = await sesi_db.execute(query)

    result_list_peminjaman_buku_id = result.scalar_one_or_none()

    if result_list_peminjaman_buku_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Peminjaman Buku Id {id} tidak ditemukan"
        )

    return ResultHpeminjaman[HPeminjamanResponse](
        status=status.HTTP_200_OK,
        pesan=f"Peminjaman Buku Id {id} ditemukan",
        data = HPeminjamanResponse.model_validate(result_list_peminjaman_buku_id)
    )


async def result_add_Hpinjam(hpeminjaman: HPeminjamanCreate, username_aktif: str, sesi_db: AsyncSession = Depends(get_database)) -> ResultHpeminjaman[HPeminjamanResponse]:
    
    if not hpeminjaman.details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="List Buku yang dipinjam tidak boleh kosong"
        )

    getMember_id = await sesi_db.get(Member, hpeminjaman.member_id)

    if not getMember_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Member id {hpeminjaman.member_id} tidak ditemukan"
        )

    try:
        set_no_pinjam = await generate_no_pinjam(sesi_db)

        total_qty = sum(item.qty for item in hpeminjaman.details)

        result_header_pinjam = HPeminjaman(
            member_id=hpeminjaman.member_id,
            no_pinjam = set_no_pinjam,
            qty_pinjam = total_qty,
            tanggal_pinjam = hpeminjaman.tanggal_pinjam,
            tanggal_kembali = hpeminjaman.tanggal_kembali,

            created_at = datetime.now(),
            created_by = username_aktif
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

            buku.qty -= item.qty

            result_detail_pinjam = DPeminjaman(
                header_id = result_header_pinjam.id,
                buku_id = item.buku_id,
                qty = item.qty,
                created_at = datetime.now(),
                created_by = username_aktif
            )

            sesi_db.add(result_detail_pinjam)

        await sesi_db.commit()

        query = (
            select(HPeminjaman)
            .options(
                selectinload(HPeminjaman.member_ref),
                selectinload(HPeminjaman.details).selectinload(DPeminjaman.buku),
            )
            .where(HPeminjaman.id == result_header_pinjam.id)
        )
        
        result = await sesi_db.execute(query)

        cek_hasil_header_pinjam = result.scalar_one()

        # cek_hasil_header_pinjam.nama_member = getMember_id.nama

        return ResultHpeminjaman[HPeminjamanResponse](
            status=status.HTTP_201_CREATED,
            pesan=f"Peminjaman buku berhasil dibuat",
            data=HPeminjamanResponse.model_validate(cek_hasil_header_pinjam)
        )

    except HTTPException:
        await sesi_db.rollback()
        raise
    
    except Exception as e:
        await sesi_db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan membuat peminjaman buku : {str(e)}"
        )
