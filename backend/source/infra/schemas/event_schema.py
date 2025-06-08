from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.source.infra.schemas.building_schema import BuildingSchema


class EventSchema(BaseModel):
    eventId: Optional[int] = None
    name: str
    eventDate: datetime
    isActive: bool
    buildingId: int
    building: Optional[BuildingSchema] = None