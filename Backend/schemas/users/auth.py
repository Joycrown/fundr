from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from config.database import Base




class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int 
    email: EmailStr



   