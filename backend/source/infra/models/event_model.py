from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class EventModel(Base):
    __tablename__ = 'event'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    eventStartDate: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    isActive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    eventBuildingId: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)
    building: Mapped["BuildingModel"] = relationship("BuildingModel", back_populates="event")