from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    userId: Optional[int] = None
    email: EmailStr
    displayName: str
    isAdmin: bool
    isLocalUser: bool


class UserResponseSchema(BaseModel):
    userId: Optional[int] = None
    email: EmailStr
    displayName: str
    isAdmin: bool
    isLocalUser: bool
    isLocalUser: bool

