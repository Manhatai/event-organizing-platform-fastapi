from datetime import datetime, timezone, timedelta

import bcrypt
import jwt
from fastapi import HTTPException

from backend.source.config.config import SECRET_KEY
from backend.source.infra.models.user_model import UserModel


def hash_password(user):
    return bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

def login_existing_check(db, user):
    existing_user = db.query(UserModel).filter(UserModel.login == user.login).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"The login '{user.login}' already exists!"
        )

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode('utf-8')
    )

def generate_auth_token(login):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload = {"user": login, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")