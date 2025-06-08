from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import (query_single_item, query_multiple_items,
                                                            update_record,
                                                            add_and_commit)
from backend.source.infra.models.user_model import UserModel
from backend.source.infra.schemas.user_schema import UserResponseSchema
from backend.source.utils.user_authentication_check.auth_check import TokenBearer

user_router = APIRouter()
token_bearer = TokenBearer()

@user_router.get("/users", response_model=list[UserResponseSchema], status_code=200)
async def get_all_users(db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> list[type[UserModel]]:
    return query_multiple_items(db, UserModel)

@user_router.get("/users/{user_id}", response_model=UserResponseSchema, status_code=200)
async def get_single_users(user_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[UserModel]:
    return query_single_item(db, UserModel, user_id, 'User', primary_key_field='userId')

@user_router.post("/users", response_model=UserResponseSchema, status_code=201)
async def create_new_users(user: UserResponseSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> UserModel:
    new_user = UserModel(
        email=user.email,
        displayName=user.displayName,
        isAdmin=user.isAdmin,
        isLocalUser=user.isLocalUser
    )
    return add_and_commit(db, new_user)

@user_router.put("/users/{user_id}", response_model=UserResponseSchema, status_code=200)
async def update_users(user_id: int, update_data:UserResponseSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)) -> type[UserModel] | None:
    return update_record(db, UserModel, update_data, user_id, 'User', primary_key_field='userId')