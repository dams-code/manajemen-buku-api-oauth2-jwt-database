from helpers.security import verify_access_token
from schemas.user import UserResponse, ResultUser
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from schemas.roles import Roles
from typing import Annotated

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_database
from models.roles import Role
from models.user import User as Model_User

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_role_user(token: Annotated[str, Depends(oauth_scheme)], sesi_db: AsyncSession = Depends(get_database))-> ResultUser[UserResponse]:
    
    # cek_username_aktif = verify_access_token(token,3600)
    cek_username_aktif = verify_access_token(token)

    if not cek_username_aktif.username:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Sesi habis, login terlebih dahulu",
            headers={"WWW-Authenticate": "Bearer"}
        )

    query = select(Model_User).where(func.lower(Model_User.username) == cek_username_aktif.username.lower())

    result = await sesi_db.execute(query)

    user = result.scalar_one_or_none()

    # user = next((user for user in data_user if user["username"].lower() == cek_username_aktif.username.lower()), None

    if user is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Username tidak ditemukan"
        )

    return ResultUser[UserResponse](
        status=status.HTTP_200_OK,
        pesan="Username ditemukan",
        data_user=UserResponse.model_validate(user)
    )
        

class CekRole:
    def __init__(self, roles: list[Roles]):
        self.roles = roles

    def __call__(self, user_role: ResultUser[UserResponse] = Depends(get_role_user)) -> str:

        user_role = user_role.data_user

        if not user_role or not user_role.role_ref:

            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak, Halaman ini dapat diakses user dengan role : {[r.value for r in self.roles]}"
            )

        return user_role.role_ref.roledesc


