from fastapi import  Depends,HTTPException,status,APIRouter,Response
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas.users import user
from schemas.admin.admin import CreateAdmin,AdminSignUp, AdminOut, AdminChangePassword
from utlis.users import utilis
from apps.users import oauth
from utlis.users.email import admin_invite
from .oauth import get_current_user_admin_login, verify_access_token_admin_enroll,verify_access_token_admin_login,create_access_token




router= APIRouter(
    tags=["Admin"]
)



"""
Admin route
To enroll an admin
"""
@router.post('/admin/enrollment',status_code=status.HTTP_201_CREATED,  response_model=AdminOut)
async def create_admin (admin: CreateAdmin, db: Session= Depends(get_db),):
    check_email = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == admin.email).first()
    if check_email: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
    check_phone_no = db.query(dbmodel.Admin).filter(dbmodel.Admin.phone_no == admin.phone_no).first()
    if check_phone_no : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
    # if current_user.role != "Super Admin" :
    #     raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail=f"You dont have access to this role")
    create_token = create_access_token({"email":admin.email,"role":admin.role})
    link = f"https://admin.myfundr.co/admin/signup/{create_token}"
    new_account = dbmodel.Admin(**admin.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    await admin_invite("Admin Invite", admin.email, {
        "title": "Admin Invite",
        "name": admin.last_name,
        "reset_link": link
    })

    return  new_account




"""
Admin route
Admin signup after invitation
"""
@router.put('/admin/signup/')
async def admin_signup (token:str, details:AdminSignUp,db: Session = Depends(get_db)):
    password_hash = utilis.hash(details.password)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
    user =  verify_access_token_admin_enroll(token,credentials_exception)
    if user.role != details.role:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You dont have access to {details.role} role")
    if user.email != details.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No Admin Right given to {details.email}")
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
    token =  verify_access_token_admin_login(access_token,credentials_exception)
    user = db.query(dbmodel.Admin).filter(dbmodel.Admin.email == token.email).first()
    return {"access_token": access_token,"token_type":"bearer","current_user":user.first_name,"role":user.role}

"""
Admin route
To load signed admin details
"""
@router.get('/admin/me', response_model=AdminOut)
async def get_current_user(db: Session = Depends(get_db),current_user: AdminOut = Depends(get_current_user_admin_login)):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"couldnt validate credentials")
  return current_user

"""
Admin route
To delete a user
"""
@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT )
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user_admin_login)):
  user= db.query(dbmodel.Users).filter(dbmodel.Users.id == id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  user.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)




"""
Admin route
To change Admin's password from profile
"""

@router.put('/admin/change_password')
async def update_user_password(details:AdminChangePassword,db: Session = Depends(get_db),current_user: AdminOut = Depends(get_current_user_admin_login)):
  check_user = db.query(dbmodel.Admin).filter(dbmodel.Admin.id == current_user.id).first()
  check_password= utilis.verify(details.current_password,current_user.password)
  if not check_password:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"current password not a match")
  hash_new_password= utilis.hash(details.new_password)
  print(hash_new_password)
  user_update= db.query(dbmodel.Admin).filter(dbmodel.Admin.id == current_user.id)
  user_update.update({"password": hash_new_password},synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_202_ACCEPTED)