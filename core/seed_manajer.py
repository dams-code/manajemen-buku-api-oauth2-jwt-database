import asyncio
import sys
from models.roles import Role
from models.user import User
from core.database import AsyncLocalSession
from helpers.helper_password_user import get_password_hash
from sqlalchemy import select
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent))

async def ManajerSeed():
    
    async with AsyncLocalSession() as sesi_db:
        try:
            cek_role = select(Role).where(Role.roledesc == "manajer")

            result = await sesi_db.execute(cek_role)

            manajer = result.scalars().first()

            if not manajer:
                print("Role manajer belum ada di table roles")
                return

            cek_user = select(User).where(User.username == "usermanajer")

            user = await sesi_db.execute(cek_user)

            hasil_cek = user.scalars().first()

            if hasil_cek:
                print("Username 'usermanajer' sudah ada di table user")
                return

            hashed_password = get_password_hash("123");

            result_registrasi_manajer = User(
                username="usermanajer",
                nama="User Manajer",
                hashed_password=hashed_password,
                created_at = datetime.now(),
                created_by="sistem",
                role_id=manajer.id
            )

            sesi_db.add(result_registrasi_manajer)
            await sesi_db.commit()
            print("Username 'usermanajer' berhasil dibuat")

        except Exception as err:
            await sesi_db.rollback()
            print(f"Proses seed data user error, {err}")

        finally:
            await sesi_db.close()

if __name__ == "__main__":
    asyncio.run(ManajerSeed())
