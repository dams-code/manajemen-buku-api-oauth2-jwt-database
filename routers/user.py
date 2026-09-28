from repositories.user import *
from repositories.roles import CekRole
from schemas.user import *
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Query

from helpers.security import *

from typing import Annotated

router_user = APIRouter(tags=["user"])

@router_user.post("/login", response_model=ResultUser[UserBase])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return await result_login(form_data=form_data)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router_user.get("/users", response_model=ResultUser[UserResponse |list[UserResponse]], dependencies=[Depends(CekRole([Roles.MANAJER]))])
# async def get_user(id: Annotated[int, Query()] = None, username: Annotated[str, Query()]=None, token: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)] = None):
async def get_user(id: Annotated[int, Query()] = None, username: Annotated[str, Query()]=None):
    return await result_get_user(id=id, username=username)

@router_user.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    
    return await result_logout(token=token)

@router_user.post("/registrasi")
async def registrasi(registrasi_user: User):

    return await result_registrasi(registrasi_user)

@router_user.post("/user", dependencies=[Depends(CekRole([Roles.MANAJER]))])
async def tambah_user(tambah_user: User):
    return await result_registrasi(tambah_user)

@router_user.get("/user/aktif", response_model=ResultUser[UserBase])
async def get_user_aktif(token: Annotated[str, Depends(oauth2_scheme)]):

    return await result_get_user_aktif(token=token)

@router_user.get("/user/{username}", response_model=ResultUser[UserResponse], dependencies=[Depends(CekRole([Roles.MANAJER]))])
async def get_user_id(username: str):
    return await result_get_user_id(username);

@router_user.put("/user/aktif/update/{username}")
async def update_user_aktif(username: str, update_user: UserUpdate, token: Annotated[str, Depends(oauth2_scheme)] = None):
    return await result_update_user_aktif(username, update_user, token)

@router_user.put("/user/update/{username}", dependencies=[Depends(CekRole([Roles.MANAJER]))])
async def update_user(username:str, update_user: UserUpdate):
    return await result_update_user(username, update_user)

@router_user.put("/user/update/password/{username}")
async def update_password(username: str, data_password: UpdatePasswordUser, token: Annotated[str, Depends(oauth2_scheme)]):
    return await result_update_password_user(username, data_password, token)

@router_user.delete("/user/{username}", dependencies=[Depends(CekRole([Roles.MANAJER]))])
async def delete_user(username: str, token: Annotated[str, Depends(oauth2_scheme)]):
    return await result_delete_user(username, token)