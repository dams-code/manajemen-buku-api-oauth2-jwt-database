
from pwdlib import PasswordHash

set_hash = PasswordHash.recommended()

def verify_password(password: str, hashed_password: str) -> bool:
    return set_hash.verify(password, hashed_password)

def get_password_hash(password: str)-> str:
    return set_hash.hash(password)