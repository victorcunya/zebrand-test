
from enum import Enum
from typing import Union

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    password: str
    expire: Union[int, None]


class UserRoleEnum(str, Enum):
    ADMIN_ROLE = 'ADMIN_ROLE'
    USER_ROLE = 'USER_ROLE'


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRoleEnum


class User(UserCreate):
    id: int
    state: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str
    password: str
