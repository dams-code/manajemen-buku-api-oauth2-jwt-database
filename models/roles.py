from sqlalchemy import ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base
from models.user import *

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    roledesc: Mapped[str] = mapped_column(String(10))

    user_ref: Mapped[list["User"]] = relationship("User", back_populates="roles_ref")
    