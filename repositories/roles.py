from repositories.user import data_user
from helpers.security import verify_access_token
from schemas.user import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from schemas.roles import Roles
from typing import Annotated

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_role_user(token: Annotated[str, Depends(oauth_scheme)])-> ResultUser[UserBase]:
    
    # cek_username_aktif = verify_access_token(token,3600)
    cek_username_aktif = verify_access_token(token)

    if not cek_username_aktif.username:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Sesi habis, login terlebih dahulu",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = next((user for user in data_user if user["username"].lower() == cek_username_aktif.username.lower()), None)

    if user is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Username tidak ditemukan"
        )

    return ResultUser[UserBase](
        status=status.HTTP_200_OK,
        pesan="Username ditemukan",
        data_user=UserBase(**user)
    )
        

class CekRole:
    def __init__(self, roles: list[Roles]):
        self.roles = roles

    def __call__(self, user_role: ResultUser[UserBase] = Depends(get_role_user)) -> str:

        user_role = user_role.data_user

        if not user_role or user_role.role not in self.roles:

            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak, Halaman ini dapat diakses user dengan role : {[r.value for r in self.roles]}"
            )

        return user_role


