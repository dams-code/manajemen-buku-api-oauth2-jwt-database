from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_database
from sqlalchemy import select, func
from models.peminjaman import HPeminjaman
from fastapi import Depends, HTTPException

async def generate_no_pinjam(sesi_db: AsyncSession = Depends(get_database)) -> str:
    tanggal_sekarang = datetime.now()

    tahunBulan = tanggal_sekarang.strftime("%Y%m")
    prefix_no_pinjam = f"PNJ-{tahunBulan}"

    query = select(HPeminjaman.no_pinjam).where(HPeminjaman.no_pinjam.like(f"{prefix_no_pinjam}%")).order_by(HPeminjaman.no_pinjam.desc()).limit(1)

    result = await sesi_db.execute(query)

    no_pinjam_terakhir = result.scalar_one_or_none()

    if no_pinjam_terakhir is None:
        seq = 1
    else:
        seq_terakhir = int(no_pinjam_terakhir[-4:])
        seq = seq_terakhir + 1

    no_pinjam_baru = f"{prefix_no_pinjam}{seq:04d}"

    return no_pinjam_baru


    