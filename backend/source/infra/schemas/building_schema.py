from typing import Optional

from pydantic import BaseModel

from backend.source.infra.schemas.region_schema import RegionSchema


class BuildingSchema(BaseModel):
    buildingId: Optional[int] = None
    name: str
    address: str
    regionId: int
    region: Optional[RegionSchema] = None
    hasOpenStands: bool