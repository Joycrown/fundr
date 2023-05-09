from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.database import get_db
from schemas.users import auth
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import dbmodel
from config.environ import settings





SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


def create_access_token(data: dict):
    to_encode= data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception ):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id = payload.get("transaction_id")
        email= payload.get("email")
        if id is None:
            raise credentials_exception
        elif email is None:
            raise credentials_exception
        token_data= auth.CryptochilData(id=id,email=email) 
    except JWTError:
        raise credentials_exception
    return token_data 