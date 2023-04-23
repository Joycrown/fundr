# from pydantic import BaseModel, EmailStr
# from typing import Optional




# class AccountCreate(BaseModel):

#     first_name: str
#     last_name: str
#     email: EmailStr
#     country: str
#     phone_no: int
#     password: str
#     transaction_id: str
#     account_purchased:str
#     time_stamp:str
#     transaction_link:str
#     status_payment: Optional[str]
   



# class StatusUpdate(BaseModel):
    
#     id: int
#     first_name: str
#     last_name: str
#     email: EmailStr
#     country: str
#     phone_no: int
#     transaction_link: str
#     account_purchased:str
#     time_stamp:str
#     transaction_link:str
#     status_payment: str





# class AccountUpdate(BaseModel):
#    account_purchased:str
#    time_stamp:str
#    transaction_link:str
   
   

# class AccountCreateOut(BaseModel):

#     id: int
#     first_name:str
#     last_name:str
#     email:EmailStr
#     country:str
#     phone_no:int
#     time_stamp:str
#     account_purchased:str
#     status_payment:str
#     transaction_id:str
#     type:str
    

#     class Config:
#         orm_mode= True



# class RejectPayment(BaseModel):
#     id: int
#     type: str
#     reason:str
#     email:EmailStr