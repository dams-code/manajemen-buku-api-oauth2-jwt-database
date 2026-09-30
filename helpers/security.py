# from itsdangerous import TimestampSigner, SignatureExpired, BadTimeSignature
from schemas.token import TokenData
from datetime import timezone, datetime, timedelta
from fastapi import HTTPException, status
from dotenv import load_dotenv

import os

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

load_dotenv()

GET_SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITM = "HS256"

if GET_SECRET_KEY is None:
    raise RuntimeError("File .env belum dibuat / tidak ditemukan")

# signer = TimestampSigner(GET_SECRET_KEY)


# def create_access_token(username: str):
#     token = signer.sign(username).decode("UTF-8")
#     return token

def create_access_token(data: dict, expires_delta: timedelta | None=None):
    encode_data = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

    if len(GET_SECRET_KEY.encode("UTF-8")) < 32:
        raise ValueError("Secret Key pendek, minimal 32 karakter")

    encode_data.update({"exp": expires})

    jwt_encode = jwt.encode(encode_data, GET_SECRET_KEY, algorithm=ALGORITM)

    return jwt_encode

# def verify_access_token(token: str, umur_token: int = 3600) -> str:
#     try:
#         username = signer.unsign(token, max_age=umur_token).decode("UTF-8")
#         return username
#     except SignatureExpired:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token sudah expired / kadaluwarsa",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except BadTimeSignature:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token tidak valid",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

def verify_access_token(token: str) -> TokenData:
    cek_kridensial = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Validasi kridensial token gagal",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, GET_SECRET_KEY, algorithms=[ALGORITM])

        username = payload.get('sub')

        if username is None:
            raise cek_kridensial

        token_data = TokenData(username=username)

        return token_data

    except ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token expired, Login terlebih dahulu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise cek_kridensial