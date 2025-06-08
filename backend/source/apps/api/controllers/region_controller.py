from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit, delete_and_commit, safe_delete_check)
from backend.source.infra.models import BuildingModel
from backend.source.infra.models.region_model import RegionModel
from backend.source.infra.schemas.region_schema import RegionSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

region_router = APIRouter()
token_bearer = TokenBearer()

@region_router.get("/regions", response_model=list[RegionSchema], status_code=200)
async def get_all_regions(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[RegionModel]]:
    return query_multiple_items(db, RegionModel)

@region_router.get("/regions/{region_id}", response_model=RegionSchema, status_code=200)
async def get_single_region(region_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[RegionModel]:
    return query_single_item(db, RegionModel, region_id, 'Region', primary_key_field='regionId')

@region_router.post("/regions", response_model=RegionSchema, status_code=201)
async def create_new_region(region: RegionSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> RegionModel:
    new_region = RegionModel(
        name=region.name,
        value=region.value
    )
    return add_and_commit(db, new_region)

@region_router.put("/regions/{region_id}", response_model=RegionSchema, status_code=200)
async def update_region(region_id: int, update_data:RegionSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[RegionModel] | None:
    return update_record(db, RegionModel, update_data, region_id, 'Region', primary_key_field='regionId')

@region_router.delete("/regions/{region_id}", status_code=204)
async def delete_region(region_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, RegionModel, region_id, 'Region', primary_key_field='regionId')
    safe_delete_check(db, BuildingModel, region_id, 'regionId', 'Region', 'Building')
    return delete_and_commit(db, item)