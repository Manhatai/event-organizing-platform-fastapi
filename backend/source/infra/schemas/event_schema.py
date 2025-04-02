from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime

from backend.source.infra.schemas.building_schema import BuildingSchema


class EventSchema(BaseModel):
    id: Optional[int] = None
    name: str
    eventStartDate: datetime
    isActive: bool
    eventBuildingId: int
    building: Optional[BuildingSchema] = None