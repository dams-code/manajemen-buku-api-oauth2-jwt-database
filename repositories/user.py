from datetime import timedelta
from helpers.security import *
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import *
from schemas.roles import *
from schemas.token import TokenData
from models.token import TokenSession
from helpers.helper_password_user import verify_password, get_password_hash

# import secrets

temp_token: dict[str, str] = {}

data_user = [
    {
        "id": 1,
        "username": "test1",
        "nama": "user test 1",
        "hash_password": get_password_hash("test1"),
        "role": "admin"
    },
    {
        "id": 2,
        "username": "test2",
        "nama": "user test 2",
        "hash_password": get_password_hash("test2"),
        "role": "manajer"
    }
]

async def result_login(form_data: OAuth2PasswordRequestForm) -> ResultUser[UserBase]:
    
    result_data_user = next((user for user in data_user if user["username"].lower() == form_data.username.lower()) ,None)

    if result_data_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Username {form_data.username} tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # user_aktif = UserInDB(**result_data_user)

    # if not verify_password(form_data.password, user_aktif.hash_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail=f"Password yang dimasukkan salah",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    if not verify_password(form_data.password, result_data_user["hash_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password yang anda masukan salah",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # secret_token = secrets.token_hex(32)
    # temp_token[secret_token] = user_aktif.username

    # access_token = create_access_token(username=form_data.username)

    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(hours=1))

    return ResultUser[UserBase](
        status=status.HTTP_200_OK,
        pesan=f"User {form_data.username} berhasil login",
        # data_user=UserBase(**user_aktif.model_dump()),
        data_user=UserBase(**result_data_user),
        data_token=TokenSession(
            # access_token=list(temp_token.keys())[0],
            access_token = access_token,
            token_type="bearer",
            username=form_data.username
        )
    )

async def result_get_user(id: int | None, username: str | None) -> ResultUser[UserResponse | list[UserResponse]]:

    # if not token:
    #     raise HTTPException(
    #         status_code= status.HTTP_401_UNAUTHORIZED,
    #         detail="Token tidak ada / wajib disertakan",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # cek_username_aktif = next((user for user in data_user if user["username"].lower() == temp_token.get(token, "").lower()), None)

    # cek_username_aktif  = verify_access_token(token, 3600)

    if id is not None or username is not None:
        result_data_user = next((user for user in data_user if (id is None or user["id"] == id) and (username is None or user["username"].lower() == username.lower()) ), None)

        if result_data_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User id {id} tidak ditemukan"
            )

        return ResultUser[UserResponse](
            status= status.HTTP_200_OK,
            pesan= f"Data user id {result_data_user['id']} - username {result_data_user['username']} berhasil terload",
            data_user= UserResponse(**result_data_user)
        )

    list_user = [UserResponse(**user) for user in data_user]

    return ResultUser[list[UserResponse]](
        status=status.HTTP_200_OK,
        pesan=f"User berhasil terload (total {len(list_user)} user)",
        data_user=list_user
    )

async def result_get_user_aktif(token: str)-> ResultUser[UserBase]:
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak ada / wajib disertakan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # cek_username_aktif = verify_access_token(token, 3600)
    cek_username_aktif = verify_access_token(token)

    get_data_username = next((user for user in data_user if user["username"].lower() == cek_username_aktif.username.lower()),None)

    if get_data_username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username tidak ada / belum registrasi"
        )

    return ResultUser[UserBase](
        status=status.HTTP_200_OK,
        pesan=f"Data user {cek_username_aktif.username} ditemukan",
        data_user=UserBase(**get_data_username)
    )

async def result_get_user_id(username: str)-> ResultUser[UserResponse]:
    
    get_data_username = next((user for user in data_user if user["username"].lower() == username.lower()),None)

    if get_data_username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username tidak ada / belum registrasi"
        )

    return ResultUser[UserResponse](
        status=status.HTTP_200_OK,
        pesan=f"Data user {username} ditemukan",
        data_user=UserResponse(**get_data_username)
    )


async def result_logout(token: str) -> ResultUser[None]:
    if token in temp_token:
        del temp_token[token]

    # cek_username_aktif  = verify_access_token(token, 3600)
    cek_username_aktif = verify_access_token(token)

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan=f"Anda sudah logout"
    )

async def result_registrasi(registrasi_user: User) :

    cek_user = next((user for user in data_user if user["username"].lower() == registrasi_user.username.lower()), None)

    if cek_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User sudah terdaftar disistem"
        )

    if not registrasi_user.password or not registrasi_user.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password User tidak boleh kosong"
        )

    Hash_password_user = get_password_hash(password=registrasi_user.password)

    if not data_user:
        id_user = 1
    else:
        list_id_user = [id_user.get("id") for id_user in data_user]

        id_user = max(list_id_user) + 1

    get_data_user = jsonable_encoder(registrasi_user)

    get_data_user.pop("password", None)

    get_data_user["id"] = id_user
    get_data_user["hash_password"] = Hash_password_user

    data_user.append(get_data_user)
    response_data_user = get_data_user.copy()
    response_data_user.pop("hash_password", None)

    return {
        "status": status.HTTP_200_OK,
        "pesan": "Registrasi / Pendaftaran User Berhasil",
        "data": response_data_user
    }


async def result_update_user_aktif(username: str, update_user: UserUpdate, token: str | None=None)-> ResultUser[None]:

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak ada / wajib disertakan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # cek_username_aktif = verify_access_token(token, 3600)
    cek_username_aktif = verify_access_token(token)

    if cek_username_aktif.username.lower() != username.lower():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username tidak sama dengan username yang aktif saat ini",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = next((user for user in data_user if user["username"].lower() == username.lower()), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} tidak ditemukan"
        )

    data_update_user =update_user.model_dump(exclude_unset=True)

    user.update(data_update_user)

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan=f"Update data user {username} berhasil"
    )

async def result_update_user(username: str, update_user: UserUpdate)-> ResultUser[None]:

    user = next((user for user in data_user if user["username"].lower() == username.lower()), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} tidak ditemukan"
        )

    data_update_user =update_user.model_dump(exclude_unset=True)

    user.update(data_update_user)

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan=f"Update data user {username} berhasil"
    )

async def result_update_password_user(username: str, data_password: UpdatePasswordUser, token: str | None=None) -> ResultUser[None]:

    if token is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak ada / wajib disertakan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # cek_username_aktif = verify_access_token(token, 3600)
    cek_username_aktif = verify_access_token(token)

    if cek_username_aktif.username.lower() != username.lower():
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Username tidak sama dengan username yang aktif saat ini",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = next((user for user in data_user if user["username"].lower() == cek_username_aktif.username.lower()), None)

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Username {username} tidak ditemukan"
        )

    if not verify_password(data_password.passwordLama, user["hash_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password yang diinput tidak sesuai dengan password lama"
        )

    password_baru = get_password_hash(data_password.passwordBaru)

    user["hash_password"] = password_baru

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan=f"Password {username} berhasil ter-update"
    )

async def result_delete_user(username: str, token: str | None=None)-> ResultUser[None]:

    # cek_username_aktif = verify_access_token(token, 3600)
    cek_username_aktif = verify_access_token(token)

    if cek_username_aktif.username == username:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User yang dihapus hanya boleh user yang tidak sedang login saat ini"
        )

    cek_index_username = next((index for index, user in enumerate(data_user) if user["username"] == username), None)

    if cek_index_username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username {username} tidak ditemukan"
        )

    del data_user[cek_index_username]

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan="Username {username} berhasil dihapus"
    )