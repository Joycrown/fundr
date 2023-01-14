from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.database import get_db
from schemas.admin.admin import AdminTokenData,AdminTokenDataLogin
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import dbmodel
from config.environ import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode= data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception ):
    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email = payload.get("email")
        role= payload.get("role")
        if email is None:
            raise credentials_exception
        elif role is None:
            raise credentials_exception
        token_data= AdminTokenData(email=email,role=role) 
    except JWTError:
        raise credentials_exception
    return token_data 


    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == token.email).first()
    return user 




def verify_access_token_login(token:str, credentials_exception ):
    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email = payload.get("email")
        id= payload.get("id")
        if email is None:
            raise credentials_exception
        elif id is None:
            raise credentials_exception
        token_data= AdminTokenDataLogin(email=email,id=id) 
    except JWTError:
        raise credentials_exception
    return token_data 


    
def get_current_user_login(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token_login(token, credentials_exception)
    user = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == token.email).first()
    return user 