from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from config.database import Base




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    is_admin: bool


# class PasswordTokenData(BaseModel):
#     id: Optional[str]
   