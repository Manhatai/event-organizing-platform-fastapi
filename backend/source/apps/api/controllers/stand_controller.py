from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit, delete_and_commit)
from backend.source.infra.models import StandModel
from backend.source.infra.schemas.stand_schema import StandSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

stand_router = APIRouter()
token_bearer = TokenBearer()

@stand_router.get("/stands", response_model=list[StandSchema], status_code=200)
async def get_all_stands(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[StandModel]]:
    return query_multiple_items(db, StandModel)

@stand_router.get("/stands/{stand_id}", response_model=StandSchema, status_code=200)
async def get_single_stand(stand_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[StandModel]:
    return query_single_item(db, StandModel, stand_id, 'Stand', primary_key_field='standId')

@stand_router.post("/stands", response_model=StandSchema, status_code=201)
async def create_new_stand(stand: StandSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> StandModel:
    new_stand = StandModel(
        name=stand.name,
        standNumber=stand.standNumber,
        categoryId=stand.categoryId,
        reservationPrice=stand.reservationPrice,
        userId=stand.userId,
        buildingId=stand.buildingId,
        reservationId=stand.reservationId
    )
    return add_and_commit(db, new_stand)

@stand_router.put("/stands/{stand_id}", response_model=StandSchema, status_code=200)
async def update_stand(stand_id: int, update_data:StandSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[StandModel] | None:
    return update_record(db, StandModel, update_data, stand_id, 'Stand', primary_key_field='standId')

@stand_router.delete("/stands/{stand_id}", status_code=204)
async def delete_stand(stand_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, StandModel, stand_id, 'Stand', primary_key_field='standId')
    return delete_and_commit(db, item)