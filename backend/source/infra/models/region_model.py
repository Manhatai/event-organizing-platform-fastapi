from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.source.infra.database.database_connection import Base


class RegionModel(Base):
    __tablename__ = 'region'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    buildingRegion: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped["BuildingModel"] = relationship("BuildingModel", back_populates="region")
