from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.source.apps.api.security.security_methods import hash_password, login_existing_check
from backend.source.infra.database.database_connection import get_db
from backend.source.infra.database.database_queries import add_and_commit
from backend.source.infra.models.user_model import UserModel
from backend.source.infra.schemas.user_schema import UserCreateSchema

user_registration_router = APIRouter()

@user_registration_router.post("/register", status_code=201)
async def user_registration(user: UserCreateSchema, db: Session = Depends(get_db)):  # Use UserCreateSchema
    login_existing_check(db, user)
    hashed_password = hash_password(user)
    new_user = UserModel(
        login=user.login,
        password=hashed_password,
        isAdmin=user.isAdmin,
        isLocalUser=user.isLocalUser
    )
    if user.email:
        new_user.email = user.email
    add_and_commit(db, new_user)
    return {"message": f"New user '{user.login}' created successfully", "user_id": new_user.id}