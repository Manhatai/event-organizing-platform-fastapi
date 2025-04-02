from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class BuildingModel(Base):
    __tablename__ = 'building'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    addressStreet: Mapped[str] = mapped_column(String, nullable=False)
    addressPostCode: Mapped[str] = mapped_column(String(9), nullable=False)
    regionId: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)
    region: Mapped["RegionModel"] = relationship("RegionModel", back_populates="building")
    hasOpenStands: Mapped[bool] = mapped_column(Boolean, nullable=False)
    stand: Mapped["StandModel"] = relationship("StandModel", back_populates='building')
    event: Mapped["EventModel"] = relationship("EventModel", back_populates='building')
