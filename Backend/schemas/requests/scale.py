from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class ScaleRequest(BaseModel):
    id:int
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[EmailStr]
    country:Optional[str]
    phone_no:Optional[int]
    role:Optional[str]
    capital:Optional[str]
    type:str
    current_capital:str
    scale_to:str
    status_scale: Optional[str]



class ScaleRequestOut(BaseModel):
    id: int
    first_name:str
    last_name:str
    email:EmailStr
    role:str
    type:str
    capital:str
    scale_to:str
    serial_no:int
    created_at:datetime
    status_scale:str


    class Config:
        orm_mode= True


class ScaleStatus(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    current_capital:str
    scale_to:str
    analytics:str
    status:str



class ScaleReject(BaseModel):
    id: int
    type: str
    reason:str
    email:EmailStr


class ScaleUpdate(BaseModel):
    id: int
    email:EmailStr
    capital:str
   