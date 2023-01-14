from fastapi import  Depends,HTTPException,status,APIRouter,Response
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from schemas.users import user
from utlis.users import utilis
from apps.users import oauth
from fastapi_pagination import Page, paginate
from utlis.users.email import send_mail, password_rest_email, rejected_payment_email
from . import oauth
from apps.admin import oauth

router= APIRouter(
    tags=["Users"]
)

"""
User sign up after purchasing an account
"""
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
async def new_user(user:user.User, db: Session= Depends(get_db)):
  hashed_password= utilis.hash(user.password)
  user.password = hashed_password
  check_email = db.query(dbmodel.Users).filter(dbmodel.Users.email == user.email).first()
  if check_email : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
  check_phone_no = db.query(dbmodel.Users).filter(dbmodel.Users.phone_no == user.phone_no).first()
  if check_phone_no : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
  new_account = dbmodel.Users(**user.dict())
  db.add(new_account)
  db.commit()
  db.refresh(new_account)
  await send_mail("Registration Successful", user.email, {
    "title": "Registration Successful",
    "name": user.last_name
  })
  return  new_account


"""
Admin route
To send User's details from liquidity provider to their account on fundr
"""
@router.put('/user_details')
async def update_user(account: user.userUpdate , db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first().status == "Rejected":
     raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"User with id: {account.id} payment has not been verified")
  account_details.update({"mt_login":account.mt_login,"mt_server":account.mt_server,
  "metatrader_password":account.metatrader_password, "analytics":account.analytics,"status":"Completed"},synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_202_ACCEPTED)


"""
Admin route
To update User's status for account 
purchasing after sending their details 
for purchase on liquidity provider
"""
@router.put('/status')
async def update_status(account: user.userStatusUpdate, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status":account.status},synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_202_ACCEPTED)
  

"""
Admin route
To reject user's account purchase if found guilty or an error is noticed
"""
@router.post('/reject')
async def reject_payment(account:user.RejectPayment,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  if check_account != account.email:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status":"Rejected","reason":account.reason},synchronize_session=False)
 
  db.commit()
  await rejected_payment_email("Payment Rejected", account.email, {
    "title": "Registration Successful",
    "name": check_account.last_name,
    "reason": account.reason
  })
  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)



"""
Admin route
To get all users on fundr system
"""
@router.get('/user/', response_model=list[user.UserOut])
def get_user(db: Session = Depends(get_db)):
  user= db.query(dbmodel.Users).order_by(dbmodel.Users.created_at).all()
  return user



"""
Admin route
To get all requests made by a user on fundr
"""
@router.get('/requests/{id}',response_model=Page[user.RequestOut])
async def get_payout_history(id: int, db: Session = Depends(get_db)):
  account_payout_history = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No request history for id: {id} yet")
  return paginate(account_payout_history)




"""
User route
To reset users password
"""
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




"""
User route
To set new user's password
"""
@router.put('/set_password' )
async def password(token:str,new_password:user.password, db: Session = Depends(get_db)):
  update_password = utilis.hash(new_password.new_password)
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
  user =  oauth.verify_access_token(token,credentials_exception)
  user_update= db.query(dbmodel.Users).filter(dbmodel.Users.id == user.id)
  user_update.update({"password": update_password},synchronize_session=False)
  db.commit()
  
  return Response(status_code=status.HTTP_202_ACCEPTED)
