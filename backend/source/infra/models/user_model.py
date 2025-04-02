from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class UserModel(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(15), nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    isAdmin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    isLocalUser: Mapped[bool] = mapped_column(Boolean, nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=True)