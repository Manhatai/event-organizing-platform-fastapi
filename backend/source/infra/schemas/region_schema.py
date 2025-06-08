from typing import Optional

from pydantic import BaseModel


class RegionSchema(BaseModel):
    regionId: Optional[int] = None
    name: str
    value: int