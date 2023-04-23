from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class UpgradeRequest(BaseModel):
    id:int
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[EmailStr]
    country:Optional[str]
    phone_no:Optional[int]
    role:Optional[str]
    capital:Optional[str]
    type:str
    current_phase:str
    upgrade_to:str
    status_upgrade: Optional[str]



class UpgradeRequestOut(BaseModel):
    id: int
    first_name:str
    last_name:str
    email:EmailStr
    role:str
    type:str
    capital:str
    current_phase:str
    serial_no:int
    created_at:datetime
    status_upgrade:str


    class Config:
        orm_mode= True


class UpgradeStatus(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    current_phase:str
    upgrade_to:str
    analytics:str
    status_upgrade:str



class UpgradeReject(BaseModel):
    id: int
    type: str
    reason:str
    email:EmailStr


class UpgradeUpdate(BaseModel):
    id: int
    email:EmailStr
    phase:str
   