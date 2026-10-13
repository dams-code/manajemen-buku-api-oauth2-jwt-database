# from schemas.buku import BukuBase, Buku, ResultBuku
from schemas.buku import BukuBase
from schemas.user import UserBase
from datetime import datetime
from core.database import get_database
from schemas.buku import *
from fastapi import status, HTTPException, Depends
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from helpers.security import verify_access_token

from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.buku import Buku

# data_buku = [
#     {
#         "id": 1,
#         "judul": "Laskar Pelangi",
#         "penulis": "Andrea hirata",
#         "tahun": 2005,
#         "genre": "novel",
#         "tersedia": True
#     },
#     {
#         "id": 2,
#         "judul": "Bumi",
#         "penulis": "Tere Liye",
#         "tahun": 2014,
#         "genre": "fantasty",
#         "tersedia": False
#     }
# ]

async def result_get_buku(id: int | None=None, judul: str | None=None, sesi_db: AsyncSession = Depends(get_database))-> ResultBuku[list[BukuBase]]:
# async def result_get_buku(id: int | None=None, judul: str | None=None, token: str | None=None) -> ResultBuku[BukuBase | list[BukuBase]]:
# async def result_get_buku(id: int | None=None, judul: str | None=None) -> ResultBuku[BukuBase | list[BukuBase]]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu"
    #     )

    # username_aktif = verify_access_token(token, 3600)
    
    query = select(Buku)
    conditions = []

    if id is not None:
        conditions.append(Buku.id == id)

    if judul is not None:
        conditions.append(Buku.judul.ilike(f"%{judul}%"))

    if conditions:
        query = query.where(or_(*conditions))

    result = await sesi_db.execute(query)

    # if id is not None or judul is not None:
    #     # result_data_buku = next((item_buku for item_buku in data_buku if (id is not None and item_buku["id"] == id) or (judul is not None and item_buku["judul"].lower() == judul.lower()) ), None)
    #     result_data_buku = next((item_buku for item_buku in data_buku if (id is not None and item_buku["id"] == id) or (judul is not None and judul.lower() in item_buku["judul"].lower()) ), None)
    
    #     if result_data_buku is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Buku id {id} tidak ditemukan"
    #         )
    
    #     return ResultBuku[BukuBase](
    #         status= status.HTTP_200_OK,
    #         pesan= f"Data buku id {result_data_buku["id"]} - judul {result_data_buku["judul"]} berhasil terload",
    #         data= BukuBase(**result_data_buku)
    #     )
    
    # list_buku = [BukuBase(**item) for item in data_buku]
    list_buku = result.scalars().all()

    if list_buku is None or len(list_buku) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data buku tidak ditemukan"
        )

    pesan = ""

    data_buku = [BukuBase.model_validate(buku) for buku in list_buku]

    if id is not None:
        pesan += f"Buku id {id} ditemukan"
    elif judul is not None:
        pesan += f"Buku dengan awalan nama {judul} ditemukan"
    else:
        pesan += f"List data buku berhasil terload (total {len(list_buku)} buku)"

    return ResultBuku[list[BukuBase]](
        status=status.HTTP_200_OK,
        pesan=pesan,
        # data=list_buku
        data=data_buku
    )
    
async def result_get_buku_id(id: int, sesi_db: AsyncSession = Depends(get_database)) -> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    # result_data_buku = next((item_buku for item_buku in data_buku if item_buku["id"] == id), None)
    
    query = select(Buku).where(Buku.id == id)

    result = await sesi_db.execute(query)

    result_data_buku = result.scalar_one_or_none()

    if result_data_buku is None:
        return ResultBuku[BukuBase](
            status = status.HTTP_404_NOT_FOUND,
            pesan = f"Buku id {id} tidak ditemukan",
            data = None
        )

    return ResultBuku[BukuBase](
        status= status.HTTP_200_OK,
        pesan= f"Data buku id {id} ditemukan",
        # data= BukuBase(**result_data_buku)
        data= BukuBase.model_validate(result_data_buku)
    )
    
async def result_add_buku(buku: BukuCreate, user_aktif: str, sesi_db: AsyncSession = Depends(get_database))-> ResultBuku[BukuCreate]:
# async def result_add_buku(buku: Buku) -> ResultBuku[BukuBase]:

    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    query = select(Buku).where(Buku.judul == buku.judul)

    result = await sesi_db.execute(query)

    cek_data_buku = result.scalar_one_or_none()

    if cek_data_buku:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"Buku berjudul '{buku.judul}' sudah ada disistem"
        )


    data_buku = buku.model_dump(exclude_unset=True)

    result_data_buku = Buku(
        **data_buku,
        created_at = datetime.now(),
        created_by=user_aktif
    )

    sesi_db.add(result_data_buku)
    
    await sesi_db.commit()
    await sesi_db.refresh(result_data_buku)

    # if not data_buku:
    #     id_buku = 1
    # else:
    #     list_id = [item_buku.get("id") for item_buku in data_buku]
    #     id_buku = max(list_id) + 1
        
    # result_data_buku = jsonable_encoder(buku)
    
    # result_data_buku["id"] = id_buku
    
    # data_buku.append(result_data_buku)
    
    return ResultBuku[BukuBase](
        status=status.HTTP_201_CREATED,
        pesan=f"Data buku baru berhasil ditambahkan ke list",
        data= BukuBase.model_validate(result_data_buku)
    )
    
async def result_update_buku(id: int, buku: BukuUpdate, user_aktif: str, sesi_db: AsyncSession = Depends(get_database))-> ResultBuku[BukuBase]:
# async def result_update_buku(id: int, buku: Buku)-> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    # index_buku = next((index_buku for index_buku, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    # if index_buku is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Buku id {id} tidak ditemukan"
    #     )
        
    # result_update_buku = jsonable_encoder(buku)
    
    # result_update_buku["id"] = id
    
    # data_buku[index_buku] = result_update_buku
    
    query = select(Buku).where(Buku.id == id)

    data_buku = await sesi_db.execute(query)

    result_data_buku = data_buku.scalars().one_or_none()

    if result_data_buku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buku id {id} tidak ditemukan"
        )

    update_data_buku = buku.model_dump(exclude_unset=True)

    for key, item in update_data_buku.items():
        setattr(result_data_buku, key, item)

    result_data_buku.modify_at = datetime.now()
    result_data_buku.modify_by = user_aktif

    await sesi_db.commit()
    await sesi_db.refresh(result_data_buku)

    return ResultBuku[BukuBase](
        status=status.HTTP_200_OK,
        pesan=f"Data buku id {id} berhasil diupdate",
        # data = BukuBase(**result_update_buku)
        data = BukuBase.model_validate(result_data_buku)
    )
    
async def result_delete_buku(id: int, sesi_db: AsyncSession = Depends(get_database)) -> ResultBuku[None]:
# async def result_delete_buku(id: int) -> ResultBuku[None]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    query = select(Buku).where(Buku.id == id)

    result = await sesi_db.execute(query)

    result_data_buku = result.scalars().first()

    if not result_data_buku:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data buku id {id} tidak ditemukan"
        )

    await sesi_db.delete(result_data_buku)

    await sesi_db.commit()

    # index_buku = next((index for index, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    # if index_buku is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Data buku id {id} tidak ditemukan"
    #     )
        
    # del data_buku[index_buku]
    
    return ResultBuku[None](
        status=status.HTTP_200_OK,
        pesan=f"Data buku Id {id} berhasil dihapus",
        data=None
    )
    
async def result_update_status_buku(id: int, tersedia: bool, user_aktif: str, sesi_db: AsyncSession) -> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    query = (
        update(Buku).where(Buku.id == id)
        .values(tersedia=tersedia, modify_at=datetime.now(), modify_by=user_aktif)
        .returning(Buku)
    )

    result = await sesi_db.execute(query)

    result_data_buku = result.scalar_one_or_none()

    if result_data_buku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data buku Id {id} tidak ditemukan"
        )

    # index_buku = next((index for index, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    await sesi_db.commit()

    # if index_buku is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Data buku Id {id} tidak ditemukan"
    #     )
        
    # data_buku[index_buku]["tersedia"] = tersedia
    
    return ResultBuku[BukuBase](
        status=status.HTTP_200_OK,
        pesan=f"Status ketersediaan buku Id {id} berhasil diupdate",
        # data= BukuBase(**data_buku[index_buku])
        data = BukuBase.model_validate(result_data_buku)
    )


