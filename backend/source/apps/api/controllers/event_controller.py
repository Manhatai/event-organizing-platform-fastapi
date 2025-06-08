from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit, delete_and_commit)
from backend.source.infra.models import EventModel
from backend.source.infra.schemas.event_schema import EventSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

event_router = APIRouter()
token_bearer = TokenBearer()

@event_router.get("/events", response_model=list[EventSchema], status_code=200)
async def get_all_events(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[EventModel]]:
    return query_multiple_items(db, EventModel)

@event_router.get("/events/{event_id}", response_model=EventSchema, status_code=200)
async def get_single_event(event_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[EventModel]:
    return query_single_item(db, EventModel, event_id, 'Event', primary_key_field='eventId')

@event_router.post("/events", response_model=EventSchema, status_code=201)
async def create_new_event(event: EventSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> EventModel:
    new_event = EventModel(
        name=event.name,
        eventDate=event.eventDate,
        isActive=event.isActive,
        buildingId=event.buildingId,
    )
    return add_and_commit(db, new_event)

@event_router.put("/events/{event_id}", response_model=EventSchema, status_code=200)
async def update_event(event_id: int, update_data:EventSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[EventModel] | None:
    return update_record(db, EventModel, update_data, event_id, 'Event', primary_key_field='eventId')

@event_router.delete("/events/{event_id}", status_code=204)
async def delete_event(event_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, EventModel, event_id, 'Event', primary_key_field='eventId')
    return delete_and_commit(db, item)