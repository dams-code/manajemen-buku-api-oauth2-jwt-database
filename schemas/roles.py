from enum import Enum
from pydantic import BaseModel, ConfigDict

class Roles(str, Enum):
    ADMIN = 'admin'
    MANAJER = 'manajer'

class RoleResponse(BaseModel):
    id: int
    roledesc: str

    model_config = ConfigDict(from_attributes=True)


