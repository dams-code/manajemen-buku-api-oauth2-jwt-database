import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from models.member import Member
from models.buku import Buku
from models.peminjaman import StatusPinjam

@pytest.mark.asyncio
async def test_add_peminjaman_buku(client: AsyncClient, async_db: AsyncSession):
    dummy_member = Member(
        id=1, 
        nama="test member", 
        alamat="semarang", 
        no_telp="081123123", 
        created_by="test user",
        modify_at= None,
        modify_by= None,
    )

    dummy_buku = Buku(
        id=4,
        judul= "test judul buku",
        penulis= "test penulis",
        tahun= 2026,
        genre= "test",
        qty=10,
        created_by= "test user",
        modify_at= None,
        modify_by= None,
    )

    async_db.add_all([dummy_member, dummy_buku])

    await async_db.commit()

    result_data_pinjam = {
        "member_id": 1,
        "qty_pinjam": 1,
        "tanggal_pinjam": "2026-10-06T10:00:00Z",
        "tanggal_kembali": "2026-10-13T10:00:00Z",
        "created_at": "2026-10-06T10:00:00Z",
        "created_by": "test user",
        "modify_at": None,
        "modify_by": None,
        "details": [
            {"buku_id": 4, "qty": 2}
        ]
    }

    response = await client.post("/peminjaman", json=result_data_pinjam)

    print(response.json())

    assert response.status_code == 201
    res_data = response.json()
    assert res_data["status"] == 201
    assert res_data["data"]["member_id"] == 1
    assert res_data["data"]["qty_pinjam"] == 2
    assert res_data["data"]["status"] == StatusPinjam.TERBUAT.value
    assert res_data["data"]["no_pinjam"].startswith("PNJ-")
    assert len(res_data["data"]["details"]) == 1

    await async_db.refresh(dummy_buku)
    assert dummy_buku.qty == 8

@pytest.mark.asyncio
async def test_add_peminjaman_buku_stok_kurang_rollback(client: AsyncClient, async_db: AsyncSession):
    dummy_member = Member(
        id=1, 
        nama="test member", 
        alamat="semarang", 
        no_telp="081123123", 
        created_by="test user",
        modify_at= None,
        modify_by= None,
    )

    dummy_buku = Buku(
        id=3,
        judul= "test judul buku",
        penulis= "test penulis",
        tahun= 2026,
        genre= "test",
        qty=1,
        created_by= "test user",
        modify_at= None,
        modify_by= None,
    )

    async_db.add_all([dummy_member, dummy_buku])

    await async_db.commit()

    result_data_rollback = {
        "member_id": 1,
        "qty_pinjam": 1,
        "tanggal_pinjam": "2026-10-06T10:00:00Z",
        "tanggal_kembali": "2026-10-13T10:00:00",
        "created_at": "2026-10-06T10:00:00Z",
        "created_by": "test user",
        "modify_at": None,
        "modify_by": None,
        "details": [
            {"buku_id": 3, "qty": 3}
        ]
    }

    response = await client.post("/peminjaman", json=result_data_rollback)

    assert response.status_code == 400

    assert "tidak mencukupi" in response.json()["pesan"]

    await async_db.refresh(dummy_buku)
    assert dummy_buku.qty == 1

@pytest.mark.asyncio
async def test_add_peminjaman_buku_tidak_ditemukan(client: AsyncClient, async_db: AsyncSession):
    dummy_member = Member(
        id=1, 
        nama="test member", 
        alamat="semarang", 
        no_telp="081123123", 
        created_by="test user",
        modify_at= None,
        modify_by= None,
    )

    async_db.add(dummy_member)

    await async_db.commit()

    result_buku_tidak_ditemukan = {
        "member_id": 1,
        "qty_pinjam": 1,
        "tanggal_pinjam": "2026-10-06T10:00:00Z",
        "tanggal_kembali": "2026-10-13T10:00:00",
        "created_at": "2026-10-06T10:00:00Z",
        "created_by": "test user",
        "modify_at": None,
        "modify_by": None,
        "details": [
            {"buku_id": 9999, "qty": 1}
        ]
    }

    response = await client.post("/peminjaman", json=result_buku_tidak_ditemukan)

    assert response.status_code == 404
    assert "tidak ditemukan" in response.json()["pesan"]

