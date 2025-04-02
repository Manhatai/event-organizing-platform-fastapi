from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit, delete_and_commit, safe_delete_check)
from backend.source.infra.models import StandModel
from backend.source.infra.models.reservation_model import ReservationModel
from backend.source.infra.schemas.reservation_schema import ReservationSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

reservation_router = APIRouter()
token_bearer = TokenBearer()

@reservation_router.get("/reservations", response_model=list[ReservationSchema], status_code=200)
async def get_all_reservations(db: Session = Depends(get_db), user_details=Depends(token_bearer))  -> list[type[ReservationModel]]:
    return query_multiple_items(db, ReservationModel)

@reservation_router.get("/reservations/{reservation_id}", response_model=ReservationSchema, status_code=200)
async def get_single_reservation(reservation_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[ReservationModel]:
    return query_single_item(db, ReservationModel, reservation_id, 'Reservation')

@reservation_router.post("/reservations", response_model=ReservationSchema, status_code=201)
async def create_new_reservation(reservation: ReservationSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> ReservationModel:
    new_reservation = ReservationModel(
        reservationTime=reservation.reservationTime
    )
    return add_and_commit(db, new_reservation)

@reservation_router.put("/reservations/{reservation_id}", response_model=ReservationSchema, status_code=200)
async def update_reservation(reservation_id: int, update_data:ReservationSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[ReservationModel] | None:
    return update_record(db, ReservationModel, update_data, reservation_id, 'Reservation')

@reservation_router.delete("/reservations/{reservation_id}", status_code=204)
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, ReservationModel, reservation_id, 'Reservation')
    safe_delete_check(db, StandModel, reservation_id, 'reservationPeriodId', 'Reservation', 'Stand')
    return delete_and_commit(db, item)