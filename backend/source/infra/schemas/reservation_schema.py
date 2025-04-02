from typing import Optional

from pydantic import BaseModel


class ReservationSchema(BaseModel):
    id: Optional[int] = None
    reservationTime: str