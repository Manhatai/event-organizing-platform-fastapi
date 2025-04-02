import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.source.config.config import SECRET_KEY


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        try:
            jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
            return creds
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token")