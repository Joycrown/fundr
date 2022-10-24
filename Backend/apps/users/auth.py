from os import access
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from config.database import engine, get_db
from schemas.users.auth import UserLogin
from models import dbmodel
from utlis.users import utilis
from . import oauth

router = APIRouter(
    tags=["Auth"]
)

@router.post('/login')
def login (details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(dbmodel.Users).filter(dbmodel.Users.email == details.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")
    
    if not utilis.verify(details.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")

    access_token= oauth.create_access_token(data={"user_id": user.id, "admin": user.is_admin})

    return {"access_token": access_token,"token_type":"bearer"}