from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class PayoutRequest(BaseModel):
    id: str
    type: str
    amount: int
    first_name:Optional[str]
    last_name:Optional[str]
    payment_method:str
    wallet_address: str
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]
    profit_share: Optional[int]
    payable_amount: Optional[int]


class PayoutReject(BaseModel):
    id:str
    email:EmailStr
    reason:str


class PayoutConfirm(BaseModel):
    id: str
    first_name: Optional[str]
    last_name:Optional[str]
    amount_requested:Optional[str]
    payable_amount: int
    payment_method:Optional[str]
    wallet_address: Optional[str]
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]





class PayoutOut(BaseModel):
    id: str
    type: str
    amount: str
    first_name:str
    serial_no:int
    last_name:str
    payment_method:str
    wallet_address: str
    profit_share: int
    payable_amount: int
    email: Optional[EmailStr]
    analytics: Optional[str]
    status: Optional[str]
    created_at: datetime

    class Config:
        orm_mode= True
