from fastapi import  Depends,HTTPException,status,APIRouter,Response
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas.users import user
from schemas.admin.admin import CreateAdmin,AdminSignUp
from utlis.users import utilis
from apps.users import oauth
from utlis.users.email import password_rest_email
from . import oauth




router= APIRouter(
    tags=["Admin"]
)



"""
Admin route
To enroll an admin
"""
@router.post('/enrollment',status_code=status.HTTP_201_CREATED)
async def create_admin (admin: CreateAdmin, db: Session= Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
    check_email = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == admin.email).first()
    
    if check_email: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
    check_phone_no = db.query(dbmodel.Admin).filter(dbmodel.Admin.phone_no == admin.phone_no).first()
    if check_phone_no : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
    if current_user.role != "super admin" :
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail=f"You dont have access to this role")
    create_token = oauth.create_access_token({"email":admin.email,"role":admin.role})
    link = f"http://localhost:8000/?token={create_token}"
    new_account = dbmodel.Admin(**admin.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    await password_rest_email("Admin Invite", admin.email, {
        "title": "Admin Invite",
        "name": admin.last_name,
        "reset_link": link
    })

    return  new_account




"""
Admin route
Admin signup after invitation
"""
@router.put('/admin/signup')
async def admin_signup (token:str, details:AdminSignUp,db: Session = Depends(get_db)):
    password_hash = utilis.hash(details.password)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    user =  oauth.verify_access_token(token,credentials_exception)
    if user.role != details.role:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail=f"You dont have access to {details.role} role")
    if user.email != details.email:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail=f"No Admin Right given to {details.email}")
    user_update= db.query(dbmodel.Admin).filter(dbmodel.Admin.email == user.email)
    user_update.update({"password": password_hash},synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_202_ACCEPTED)




"""
Admin route
To login an admin
"""
@router.post('/admin/login')
async def admin_login (details: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == details.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")
    
    if not utilis.verify(details.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Details")

    access_token = oauth.create_access_token({"email":details.username,"id":user.id})
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token =  oauth.verify_access_token_login(access_token,credentials_exception)
    user = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == token.email).first()
    return {"access_token": access_token,"token_type":"bearer","current_user":user.first_name,"role":user.role}



"""
Admin route
To delete a user
"""
@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT )
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user_login)):
  user= db.query(dbmodel.Users).filter(dbmodel.Users.id == id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  user.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)