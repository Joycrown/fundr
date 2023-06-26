from fastapi import  Depends,HTTPException,status,APIRouter,Response, Query
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import or_
from schemas.users import user

from datetime import datetime
from fastapi_pagination import Page, paginate
from utlis.users.email import  rejected_payment_email,account_confirmation,account_setup

from apps.admin.oauth import get_current_user_admin_login

router= APIRouter(
    tags=["Admin Work"]
)

# """
# User sign up after purchasing an account
# """
# @router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
# async def new_user(user:user.User, db: Session= Depends(get_db)):
#   hashed_password= utilis.hash(user.password)
#   user.password = hashed_password
#   check_email = db.query(dbmodel.Users).filter(dbmodel.Users.email == user.email).first()
#   if check_email : 
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
#   check_phone_no = db.query(dbmodel.Users).filter(dbmodel.Users.phone_no == user.phone_no).first()
#   if check_phone_no : 
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
#   new_account = dbmodel.Users(**user.dict())
#   db.add(new_account)
#   db.commit()
#   db.refresh(new_account)
#   await account_purchased("Registration Successful", user.email, {
#     "title": "Account Purchase Successful",
#     "name": user.first_name,
#     "account": user.capital,
#   })
#   return  new_account


"""
Admin route
To send User's details from liquidity provider to their account on fundr
"""
@router.put('/user/user_details')
async def update_user(account: user.userUpdate , db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first().status == "Rejected":
     raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"User with id: {account.id} payment has not been verified")
  account_details.update({"mt_server":account.mt_server,
  "metatrader_password":account.metatrader_password,"type_meta":account.type_meta, "account_id_meta":account.account_id_meta, "analytics":account.analytics,"status":"Completed"},synchronize_session=False)
  db.commit()
  await account_setup(" Account Setup Complete", account.email, {
    "title": " Account Setup Complete",
    "name": account.first_name,
    "metatraderId" : account.mt_login,
    "password": account.metatrader_password,
    "server": account.mt_server
    
  })
  return Response(status_code=status.HTTP_202_ACCEPTED)


"""
Admin route
To update User's status for account 
purchasing after sending their details 
for purchase on liquidity provider
"""
@router.put('/user/status')
async def update_status(account: user.userStatusUpdate, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status":account.status},synchronize_session=False)
  db.commit()
  await account_confirmation("Account Purchase Confirmed", account.email, {
    "title": "Account Purchase Confirmed",
    "name": account.first_name,
    
  })
  return Response(status_code=status.HTTP_202_ACCEPTED)
  

"""
Admin route
To reject user's account purchase if found guilty or an error is noticed
"""
@router.post('/user/reject')
async def reject_payment(account:user.RejectPayment,db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  # if account.email != check_account:
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status":"Rejected","reason":account.reason},synchronize_session=False)
 
  db.commit()
  await rejected_payment_email("Payment Rejected", account.email, {
    "title": "Registration Successful",
    "name": check_account.first_name,
    "reason": account.reason,
    "account": check_account.capital
  })
  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)

"""
Admin route
To get a single user on fundr by id
"""
@router.get('/user/{id}',response_model=user.UserOut)
async def get_user(id: str, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  user_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == id).first()
  if not user_details:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with: {id} found")
  return user_details


"""
Admin route
To get all received users request for fundr 
"""
@router.get("/user/payment/pending", response_model=Page[user.UserOut])
async def get_all_users_payment_request_pending( db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  users = db.query(dbmodel.Users).filter(or_(dbmodel.Users.status == "Pending", 
  dbmodel.Users.status_scale == "Pending", 
  dbmodel.Users.status_upgrade == "Pending")).all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payment Request Received Yet")
  return paginate(users)


"""
Admin route
To get all completed or rejected users request/payment on fundr 
"""
@router.get("/user/users/completed/", response_model=Page[user.RequestOut])
async def get_all_users_payment_or_request_completed_or_rejected( search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None), start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  query = db.query(dbmodel.Requests).filter(or_(
  dbmodel.Requests.status_scale == "Confirmed", dbmodel.Requests.status_scale == "Rejected", 
  dbmodel.Requests.status_upgrade == "Confirmed",dbmodel.Requests.status_upgrade == "Rejected"))
  if search_query:
       query = query.filter(
            (dbmodel.Requests.first_name.ilike(f"%{search_query}%")) |
            (dbmodel.Requests.email.ilike(f"%{search_query}%")) |
            (dbmodel.Requests.type.ilike(f"%{filter_query}%"))|
            (dbmodel.Requests.last_name.ilike(f"%{search_query}%"))
        )
  if filter_query:
       query = query.filter(
            (dbmodel.Requests.scale_to.match(f"%{filter_query}%"))|
            (dbmodel.Requests.upgrade_to.ilike(f"%{filter_query}%"))|
            (dbmodel.Requests.role.match(f"%{filter_query}%"))
        )
  if start_date:
    start_date = datetime.fromisoformat(start_date)
    query = query.filter(dbmodel.Requests.created_at >= start_date)
  if end_date:
    end_date = datetime.fromisoformat(end_date)
    query = query.filter(dbmodel.Requests.created_at <= end_date)
  users = query.all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Request found")
  return paginate(users)



"""
Admin route
To get all received request both upgrade and scaling for fundr 
"""
@router.get("/user/requests/received", response_model=Page[user.RequestOut])
async def get_all_users_request_received( db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  users = db.query(dbmodel.Requests).filter(or_(dbmodel.Requests.status_upgrade == "Received", 
  dbmodel.Requests.status_scale == "Received")).all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Request Received Yet")
  return paginate(users)


"""
Admin route
To get all received payment request for fundr 
"""

@router.get('/user/payment/received', response_model=Page[user.UserOut])
async def get_all_users_payment_request_received(db:Session= Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  users = db.query(dbmodel.Users).filter(dbmodel.Users.status == "Received").all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payment Request Received Yet")
  return paginate(users)




"""
Admin route
To get all users on fundr system
"""
@router.get("/user/", response_model=Page[user.UserOut])
def get_all_user(search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None), start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
    query = db.query(dbmodel.Users).order_by(dbmodel.Users.created_at)
    if search_query:
       query = query.filter(
            (dbmodel.Users.first_name.ilike(f"%{search_query}%")) |
            (dbmodel.Users.email.ilike(f"%{search_query}%")) |
            (dbmodel.Users.last_name.ilike(f"%{search_query}%"))
        )
    if filter_query:
       query = query.filter(
            (dbmodel.Users.capital.match(f"%{filter_query}%"))|
            (dbmodel.Users.phase.match(f"%{filter_query}%"))|
            (dbmodel.Users.role.match(f"%{filter_query}%"))
        )
    if start_date:
      start_date = datetime.fromisoformat(start_date)
      query = query.filter(dbmodel.Users.created_at >= start_date)
    if end_date:
      end_date = datetime.fromisoformat(end_date)
      query = query.filter(dbmodel.Users.created_at <= end_date)
    users = query.all()
    if not users :
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with the given search criteria")
    return paginate(users)
"""
Admin route
To get all users completed status on fundr system
"""
@router.get("/user/status/completed/", response_model=Page[user.UserOut])
def get_all_user_status_completed(search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None), start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
    query = db.query(dbmodel.Users).filter(or_(dbmodel.Users.status == "Completed", 
    dbmodel.Users.status== "Rejected", 
    ))
    if search_query:
       query = query.filter(
            (dbmodel.Users.first_name.ilike(f"%{search_query}%")) |
            (dbmodel.Users.email.ilike(f"%{search_query}%")) |
            (dbmodel.Users.last_name.ilike(f"%{search_query}%"))
        )
    if filter_query:
       query = query.filter(
            (dbmodel.Users.capital.match(f"%{filter_query}%"))|
            (dbmodel.Users.phase.match(f"%{filter_query}%"))|
            (dbmodel.Users.role.match(f"%{filter_query}%"))
        )
    if start_date:
      start_date = datetime.fromisoformat(start_date)
      query = query.filter(dbmodel.Users.created_at >= start_date)
    if end_date:
      end_date = datetime.fromisoformat(end_date)
      query = query.filter(dbmodel.Users.created_at <= end_date)
    users = query.all()
    if not users :
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with the given search criteria")
    return paginate(users)


# """
# User route
# To load signed in user details
# """
# @router.get('/user/me', response_model=user.UserOut)
# async def get_current_user(db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
#   if not current_user:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with the given search criteria")
#   return current_user



"""
Admin route
To get all requests on fundr system
"""
@router.get("/requests/", response_model=list[user.RequestOut])
def get_all_requests(search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None),start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
    query = db.query(dbmodel.Requests).order_by(dbmodel.Requests.created_at)
    if search_query:
       query = query.filter(
            (dbmodel.Users.first_name.ilike(f"%{search_query}%")) |
            (dbmodel.Users.email.ilike(f"%{search_query}%")) |
            (dbmodel.Users.last_name.ilike(f"%{search_query}%"))
        )
    if filter_query:
       query = query.filter(
            (dbmodel.Users.capital.match(f"%{filter_query}%"))|
            (dbmodel.Users.phase.match(f"%{filter_query}%"))|
            (dbmodel.Users.role.match(f"%{filter_query}%"))
        )
    if start_date:
      start_date = datetime.fromisoformat(start_date)
      query = query.filter(dbmodel.Users.created_at >= start_date)
    if end_date:
      end_date = datetime.fromisoformat(end_date)
      query = query.filter(dbmodel.Users.created_at <= end_date)
    users = query.all()
    if not users :
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with the given search criteria")
    return users







"""
Admin route
To get a single upgrade request made by a user on fundr
"""
@router.get('/user/requests/serial_no/{id}',response_model=user.RequestOut)
async def get_particular_request_with_serial_no(id: str, serial_no:int, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_payout_history = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No request history for id: {id} yet")
  request = db.query(dbmodel.Requests).filter(dbmodel.Requests.serial_no == serial_no).first()
  return request

   
"""
Admin route
To get a particular upgrade request made by a user on fundr with
"""
@router.get('/requests/{id}',response_model=Page[user.RequestOut])
async def get_a_user_request_history(id: str, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_payout_history = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No request history for id: {id} yet")
  return paginate(account_payout_history)




# """
# User route
# To reset users password
# """
# @router.post('/password')
# async def password_rest(email: user.passwordRest, db: Session = Depends(get_db)):
#   email_exist= db.query(dbmodel.Users).filter(dbmodel.Users.email == email.email).first()
#   if email_exist is not None :
#     token = oauth.create_access_token(data={"user_id": email_exist.id, "admin": email_exist.is_admin})
#     reset_link = f"http://localhost:8000/?token={token}"
#     await password_rest_email("Password Reset", email_exist.email,{
#       "title": "Password Rest",
#       "name": email_exist.last_name,
#       "reset_link": reset_link
#     })
#   else:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the {email} not found")




# """
# User route
# To set new user's password
# """
# @router.put('/set_password' )
# async def password(token:str,new_password:user.password, db: Session = Depends(get_db)):
#   update_password = utilis.hash(new_password.new_password)
#   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#     detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
#   user =  oauth.verify_access_token(token,credentials_exception)
#   user_update= db.query(dbmodel.Users).filter(dbmodel.Users.id == user.id)
#   user_update.update({"password": update_password},synchronize_session=False)
#   db.commit()
  
#   return Response(status_code=status.HTTP_202_ACCEPTED)

# """
# User route
# To change user's password from profile
# """

# @router.put('/change_password')
# async def update_user_password(details:user.ChangePassword,db: Session = Depends(get_db),current_user: user.UserOut = Depends(get_current_user)):
#   check_user = db.query(dbmodel.Users).filter(dbmodel.Users.id == current_user.id).first()
#   check_password= utilis.verify(details.current_password,current_user.password)
#   if not check_password:
#      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"current password not a match")
#   hash_new_password= utilis.hash(details.new_password)
#   print(hash_new_password)
#   user_update= db.query(dbmodel.Users).filter(dbmodel.Users.id == current_user.id)
#   user_update.update({"password": hash_new_password},synchronize_session=False)
#   db.commit()
#   return Response(status_code=status.HTTP_202_ACCEPTED)


# """
# Payouts 
# """


