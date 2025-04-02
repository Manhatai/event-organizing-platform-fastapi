# backend/source/apps/api/security/login.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.source.apps.api.security.security_methods import verify_password, generate_auth_token
from backend.source.infra.database.database_connection import get_db
from backend.source.infra.models.user_model import UserModel
from backend.source.infra.schemas.user_schema import UserLoginSchema

user_login_router = APIRouter()

@user_login_router.post("/login", status_code=200)
async def user_login(user: UserLoginSchema, db: Session = Depends(get_db)):  # Use UserLoginSchema
    potential_user = db.query(UserModel).filter(UserModel.login == user.login).first()
    if not potential_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with login '{user.login}' doesn't exist!"
        )

    if not verify_password(user.password, potential_user.password):
        raise HTTPException(status_code=400, detail="Invalid password!")

    token = generate_auth_token(potential_user.login)

    return {"token": token, "user": potential_user.login}