from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class ReservationModel(Base):
    __tablename__ = 'reservation'
    reservationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    stand: Mapped["StandModel"] = relationship("StandModel", back_populates='reservation')