from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class StandModel(Base):
    __tablename__ = 'stand'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    standNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    categoryId: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    category: Mapped["CategoryModel"] = relationship("CategoryModel", back_populates="stand")
    reservationPrice: Mapped[int] = mapped_column(Integer, nullable=False)
    bookedByUserId: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    eventBuildingId: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)
    building: Mapped["BuildingModel"] = relationship("BuildingModel", back_populates='stand')
    reservationPeriodId: Mapped[int] = mapped_column(ForeignKey("reservation.id"), nullable=True)
    reservation: Mapped["ReservationModel"] = relationship("ReservationModel", back_populates='stand')

