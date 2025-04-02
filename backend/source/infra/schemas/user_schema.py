from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateSchema(BaseModel):
    login: str
    password: str
    isAdmin: bool
    isLocalUser: bool
    email: Optional[EmailStr] = None


class UserLoginSchema(BaseModel):
    login: str
    password: str


class UserResponseSchema(BaseModel):
    id: int
    login: str
    isAdmin: bool
    isLocalUser: bool
    email: Optional[EmailStr] = None