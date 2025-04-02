from typing import Optional

from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: Optional[int] = None
    buildingRegion: str