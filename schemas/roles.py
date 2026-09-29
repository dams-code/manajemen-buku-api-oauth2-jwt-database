from enum import Enum
from pydantic import BaseModel

class Roles(str, Enum):
    ADMIN = 'admin'
    MANAJER = 'manajer'

class RoleResponse(BaseModel):
    id: int
    roledesc: str


