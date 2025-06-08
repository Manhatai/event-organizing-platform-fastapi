from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.source.infra.database.database_connection import Base


class UserModel(Base):
    __tablename__ = 'user'
    userId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    displayName: Mapped[str] = mapped_column(String(30), nullable=False)
    isAdmin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    isLocalUser: Mapped[bool] = mapped_column(Boolean, nullable=False)
