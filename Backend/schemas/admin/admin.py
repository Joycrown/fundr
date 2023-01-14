from pydantic import BaseModel, EmailStr





class CreateAdmin(BaseModel):
    first_name : str
    last_name: str
    email: EmailStr
    phone_no: int
    role: str

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