from typing import Optional

from pydantic import BaseModel

from backend.source.infra.schemas.region_schema import RegionSchema


class BuildingSchema(BaseModel):
    id: Optional[int] = None
    name: str
    addressStreet: str
    addressPostCode: str
    regionId: int
    region: Optional[RegionSchema] = None
    hasOpenStands: bool