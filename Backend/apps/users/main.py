from fastapi import  Depends,HTTPException,status,APIRouter,Response
from models import dbmodel
from config.database import engine, get_db
from sqlalchemy.orm import Session 
from schemas.users import user
from typing import List
from utlis.users import utilis
from apps.users import oauth
from utlis.users.email import send_mail, password_rest_email
from . import oauth

router= APIRouter(
    tags=["Users"]
)



@router.post('/signup',status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
async def create_User(user: user.UserCreate, db: Session = Depends(get_db)):
  hashed_password= utilis.hash(user.password)
  user.password = hashed_password
  check_email = db.query(dbmodel.Users).filter(dbmodel.Users.email == user.email).first()
  if check_email : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
  check_phone_no = db.query(dbmodel.Users).filter(dbmodel.Users.phone_no == user.phone_no).first()
  if check_phone_no : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
  await send_mail("Registration Successful", user.email, {
    "title": "Registration Successful",
    "name": user.last_name
  })
  new_user = dbmodel.Users(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return  new_user





@router.get('/user/{id}', response_model=user.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
  user= db.query(dbmodel.Users).filter(dbmodel.Users.id == id).first()
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  return user




@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT )
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
  user= db.query(dbmodel.Users).filter(dbmodel.Users.id == id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  user.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post('/password')
async def password_rest(email: user.passwordRest, db: Session = Depends(get_db)):
  email_exist= db.query(dbmodel.Users).filter(dbmodel.Users.email == email.email).first()
  if email_exist is not None :
    token = oauth.create_access_token(data={"user_id": email_exist.id, "admin": email_exist.is_admin})
    reset_link = f"http://localhost:8000/?token={token}"
    await password_rest_email("Password Reset", email_exist.email,{
      "title": "Password Rest",
      "name": email_exist.last_name,
      "reset_link": reset_link
    })
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the {email} not found")





@router.put('/set_password' )
async def password(token:str,new_password:user.password, db: Session = Depends(get_db)):
  # request_data= {k: v for k, v in new_password.dict().items() if v is not None}
  update_password = utilis.hash(new_password.new_password)
  print(update_password)
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
  user =  oauth.verify_access_token(token,credentials_exception)
  user_update= db.query(dbmodel.Users).filter(dbmodel.Users.id == user.id)
  user_update.update({"password": update_password},synchronize_session=False)
  db.commit()
  
  return Response(status_code=status.HTTP_202_ACCEPTED)
