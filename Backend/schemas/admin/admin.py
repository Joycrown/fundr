from pydantic import BaseModel, EmailStr





class CreateAdmin(BaseModel):
    first_name : str
    last_name: str
    email: EmailStr
    phone_no: int
    role: str


class AdminOut(BaseModel):
    first_name : str
    last_name: str
    email: EmailStr
    phone_no: int
    role: str
    class Config:
        orm_mode= True



class AdminSignUp(BaseModel):
    password:str
    email: EmailStr
    role: str

class AdminTokenData(BaseModel):
   email:EmailStr
   role:str


class AdminTokenDataLogin(BaseModel):
   email:EmailStr
   id:int


class AdminChangePassword(BaseModel):
    current_password:str
    new_password:str
