from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReservationSchema(BaseModel):
    reservationId: Optional[int] = None
    name: str
    value: int