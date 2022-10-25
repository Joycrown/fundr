from datetime import datetime
import email
from pydantic import BaseModel, EmailStr

from config.database import Base



class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    password: str
    transaction_id: str
    # is_admin: bool =False

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    transaction_id: str
    is_admin: bool
    created_at: datetime


    class Config:
        orm_mode= True
