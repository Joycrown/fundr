from fastapi import  Depends,HTTPException,status,APIRouter
from models import dbmodel
from config.database import engine, get_db
from sqlalchemy.orm import Session 
from schemas.users import user
from typing import List
from utlis.users import utilis
from apps.users import oauth

router= APIRouter(
    tags=["Users"]
)



@router.post('/signup',status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
def create_User(user: user.UserCreate, db: Session = Depends(get_db)):
  hashed_password= utilis.hash(user.password)
  user.password = hashed_password
  new_user = dbmodel.Users(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return  new_user


@router.get('/user/{id}', response_model=user.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
  current_user= db.query(dbmodel.Users).filter(dbmodel.Users.id == id).first()
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  return current_user