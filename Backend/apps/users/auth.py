from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from config.database import get_db
from models import dbmodel
from utlis.users import utilis
from apps.users.oauth import verify_access_token, create_access_token

router = APIRouter(
    tags=["Auth"]
)

@router.post('/login', )
def login (details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(dbmodel.Users).filter(dbmodel.Users.email == details.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")
    
    if not utilis.verify(details.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")

    access_token= create_access_token(data={"user_id": user.id, "email": user.email})
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(access_token, credentials_exception)
    user = db.query(dbmodel.Users).filter(dbmodel.Users.id == token.id).first()
    return {"access_token": access_token,"token_type":"bearer","current_user":user.first_name}



@router.get('/token/',status_code=status.HTTP_200_OK, )
def login (token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    user = verify_access_token(token, credentials_exception)
    verify_user = db.query(dbmodel.Users).filter(dbmodel.Users.id ==user.id ).first()
    return Response(status_code=status.HTTP_200_OK)