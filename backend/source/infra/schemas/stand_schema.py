from typing import Optional

from pydantic import BaseModel

from backend.source.infra.schemas.building_schema import BuildingSchema
from backend.source.infra.schemas.category_schema import CategorySchema
from backend.source.infra.schemas.reservation_schema import ReservationSchema
from backend.source.infra.schemas.user_schema import UserResponseSchema


class StandSchema(BaseModel):
    id: Optional[int] = None
    name: str
    standNumber: int
    reservationPrice: int
    categoryId: int
    category: Optional[CategorySchema] = None
    bookedByUserId: int | None = None
    user: Optional[UserResponseSchema] = None # do wywalenia pozniej
    eventBuildingId: int
    building: Optional[BuildingSchema] = None
    reservationPeriodId: int | None = None
    reservation: Optional[ReservationSchema] = None
