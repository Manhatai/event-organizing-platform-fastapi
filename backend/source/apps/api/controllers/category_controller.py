from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit, delete_and_commit, safe_delete_check)
from backend.source.infra.models import StandModel
from backend.source.infra.models.category_model import CategoryModel
from backend.source.infra.schemas.category_schema import CategorySchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

category_router = APIRouter()
token_bearer = TokenBearer()

@category_router.get("/categories", response_model=list[CategorySchema], status_code=200)
async def get_all_categories(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[CategoryModel]]:
    return query_multiple_items(db, CategoryModel)

@category_router.get("/categories/{category_id}", response_model=CategorySchema, status_code=200)
async def get_single_category(category_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[CategoryModel]:
    return query_single_item(db, CategoryModel, category_id, 'Category', primary_key_field='categoryId')

@category_router.post("/categories", response_model=CategorySchema, status_code=201)
async def create_new_category(category: CategorySchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> CategoryModel:
    new_category = CategoryModel(
        name=category.name,
        value=category.value
    )
    return add_and_commit(db, new_category)

@category_router.put("/categories/{category_id}", response_model=CategorySchema, status_code=200)
async def update_category(category_id: int, update_data:CategorySchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[CategoryModel] | None:
    return update_record(db, CategoryModel, update_data, category_id, 'Category', primary_key_field='categoryId')

@category_router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    item = query_single_item(db, CategoryModel, category_id, 'Category', primary_key_field='categoryId')
    safe_delete_check(db, StandModel, category_id, 'categoryId', 'Category', 'Stand')
    return delete_and_commit(db, item)