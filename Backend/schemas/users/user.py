from datetime import datetime
import email
from typing import Optional,List
from pydantic import BaseModel, EmailStr

from config.database import Base







class User(BaseModel):
    
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    transaction_id: str
    transaction_link: str
    capital:str
    password:str


    
class PaymentReceivedOut(BaseModel):
    id:int
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    status: str
    status_upgrade: str
    status_scale: str
    created_at: datetime
    transaction_id: str
    transaction_link: str
    capital:str
    class Config:
        orm_mode= True
    
class RequestOut(BaseModel):
    serial_no: int
    id: int
    first_name:str
    last_name:str
    email:str
    role:str
    type:str
    capital: str
    scale_to:str
    analytics:str
    status_scale:str
    current_phase:str
    upgrade_to:str
    status_upgrade:str
    reason:str
    created_at: datetime
    
    class Config:
        orm_mode= True

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    account_id_meta : str
    type_meta:str
    metatrader_password:str
    mt_server:str
    created_at: datetime
    role: str
    analytics:str
    capital: str
    upgrade_to:str
    scale_to:str
    mt_login:str
    phase: str
    country: str
    status:str
    status_upgrade:str
    status_scale:str
    transaction_id: str
    transaction_link: str
    phone_no: int
    email: EmailStr
    # request: RequestOut
    class Config:
        orm_mode= True
   


class UserOut2(BaseModel):
    user: List[UserOut]
    class Config:
        orm_mode= True

class userStatusUpdate(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    transaction_link: str
    account_purchased:str
    time_stamp:str
    transaction_link:str
    status: str



class userUpdate(BaseModel):
    id: int
    first_name:str
    last_name:str
    email:EmailStr
    country:str
    phone_no: int
    role:str
    capital:str
    phase:str
    mt_login:str
    metatrader_password:str
    mt_server:str
    analytics: str

class RejectPayment(BaseModel):
    id: int
    reason:str
    email:EmailStr
    status: Optional [str]


class passwordRest(BaseModel):
    email: str
    
class password(BaseModel):
    new_password:str


class ChangePassword(BaseModel):
    current_password:str
    new_password:str



    

class UserCreateOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    phone_no: int
    
    transaction_id: str
    transaction_link: str
    capital:str
    password:str
    class Config:
        orm_mode= True