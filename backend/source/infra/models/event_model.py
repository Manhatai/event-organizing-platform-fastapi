from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class EventModel(Base):
    __tablename__ = 'event'
    eventId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    eventDate: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    isActive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    buildingId: Mapped[int] = mapped_column(ForeignKey("building.buildingId"), nullable=False)
    building: Mapped["BuildingModel"] = relationship("BuildingModel", back_populates="event")