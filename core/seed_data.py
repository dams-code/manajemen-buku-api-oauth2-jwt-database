import asyncio
from models.roles import Role
from core.database import AsyncLocalSession
from sqlalchemy import select

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

async def RoleSeed():

    async with AsyncLocalSession() as sesi_db:
        try:
            list_role = ["admin", "manajer"]

            for nama_role in list_role:

                query = select(Role).where(Role.roledesc == nama_role)

                result = await sesi_db.scalars(query)

                cek_role = result.first()

                if not cek_role:
                    role_baru = Role(roledesc= nama_role)
                    sesi_db.add(role_baru)
                    print(f"Role {nama_role} berhasil ditambahkan ke table role")
                else:
                    print(f"Role {nama_role} sudah ada di table role.")

            await sesi_db.commit()

            print("Seed data role ke table role selesai.")
        except Exception as err:
            await sesi_db.rollback()
            print(f"Proses seed data role error, {err}")

if __name__ == "__main__":
    asyncio.run(RoleSeed())