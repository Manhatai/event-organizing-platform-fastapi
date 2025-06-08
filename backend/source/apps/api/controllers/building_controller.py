from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            safe_delete_check, update_record,
                                                            add_and_commit, delete_and_commit)
from backend.source.infra.models import BuildingModel, StandModel, EventModel
from backend.source.infra.schemas.building_schema import BuildingSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

building_router = APIRouter()
token_bearer = TokenBearer()

@building_router.get("/buildings", response_model=list[BuildingSchema], status_code=200)
async def get_all_buildings(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[BuildingModel]]:
    return query_multiple_items(db, BuildingModel)

@building_router.get("/buildings/{building_id}", response_model=BuildingSchema, status_code=200)
async def get_single_building(building_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[BuildingModel]:
    return query_single_item(db, BuildingModel, building_id, 'Building', primary_key_field='buildingId')

@building_router.post("/buildings", response_model=BuildingSchema, status_code=201)
async def create_new_building(building: BuildingSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> BuildingModel:
    new_building = BuildingModel(
        name=building.name,
        address=building.address,
        regionId=building.regionId,
        hasOpenStands=building.hasOpenStands,
    )
    return add_and_commit(db, new_building)

@building_router.put("/buildings/{building_id}", response_model=BuildingSchema, status_code=200)
async def update_building(building_id: int, update_data:BuildingSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[BuildingModel] | None:
    return update_record(db, BuildingModel, update_data, building_id, 'Building', primary_key_field='buildingId')

@building_router.delete("/buildings/{building_id}", status_code=204)
async def delete_building(building_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, BuildingModel, building_id, 'Building', primary_key_field='buildingId')
    safe_delete_check(db, StandModel, building_id, 'buildingId', 'Building', 'Stand')
    safe_delete_check(db, EventModel, building_id, 'buildingId', 'Building', 'Event')
    return delete_and_commit(db, item)