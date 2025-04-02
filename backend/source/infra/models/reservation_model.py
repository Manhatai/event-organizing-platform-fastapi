from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class ReservationModel(Base):
    __tablename__ = 'reservation'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reservationTime: Mapped[str] = mapped_column(String, nullable=False)
    stand: Mapped["StandModel"] = relationship("StandModel", back_populates='reservation')