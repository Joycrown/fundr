from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class PayoutRequest(BaseModel):
    id: int
    type: str
    amount: str
    first_name:Optional[str]
    last_name:Optional[str]
    payment_method:str
    wallet_address: str
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]


class PayoutReject(BaseModel):
    id:int
    email:EmailStr
    reason:str


class PayoutConfirm(BaseModel):
    id: int
    first_name: Optional[str]
    last_name:Optional[str]
    amount_requested:Optional[str]
    profit_split: str
    payment_method:Optional[str]
    wallet_address: Optional[str]
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]




class PayoutOut(BaseModel):
    id: int
    type: str
    amount: str
    first_name:str
    serial_no:int
    last_name:str
    payment_method:str
    wallet_address: str
    profit_share: str
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]
    created_at: datetime

    class Config:
        orm_mode= True
