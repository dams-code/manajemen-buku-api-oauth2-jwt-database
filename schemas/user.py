from schemas.roles import RoleResponse
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Generic, Optional, TypeVar
from models.token import TokenSession

T = TypeVar('T')

class UserBase(BaseModel):
    username: str
    nama: str
    # role: str
    role_id: int
    created_at: datetime
    created_by: str
    modify_at: datetime | None
    modify_by: str

    model_config = ConfigDict(from_attributes=True)
    
class User(UserBase):
    password: str
    
class UserInDB(UserBase):
    hash_password: str

class UserResponse(UserBase):
    id: int
    role_ref: RoleResponse

class UserCreate(BaseModel):
    username: str
    nama: str
    # role: str
    password: str
    role_id: int

class UserUpdate(BaseModel):
    # id: int
    nama: Optional[str] = None
    # role: Optional[str] = None
    role_id: Optional[int] = None

class UpdatePasswordUser(BaseModel):
    passwordLama: str
    passwordBaru: str

class ResultUser(BaseModel, Generic[T]):
    status: int
    pesan: str
    data_user: Optional[T] = None
    data_token: Optional[TokenSession] = None

