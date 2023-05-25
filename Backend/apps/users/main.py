from fastapi import  Depends,HTTPException,status,APIRouter,Response
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import or_
from schemas.users import user
from utlis.users import utilis
from apps.users import oauth
from apps.cyptochil.cryptochilSignUp import verify_access_token
from apps.cyptochil.cyptochil import cryptochill_api_request
from utlis.users.email import account_purchased, password_rest_email
from apps.users import oauth
import random
router= APIRouter(
    tags=["Users"]
)

"""
User sign up after purchasing an account
"""
def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for i in range(n_digits)])
    return f"{prefix}{random_digits}"

@router.post('/signup/', status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
async def new_user(user:user.User, token:str, db: Session= Depends(get_db)):
  hashed_password= utilis.hash(user.password)
  user.password = hashed_password
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"couldnt validate credentials", headers={"WWW-Authenticate":"Bearer"})
  check_user = verify_access_token(token,credentials_exception)
  check_email = db.query(dbmodel.Users).filter(dbmodel.Users.email == check_user.email).first()
  if check_email : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
  check_phone_no = db.query(dbmodel.Users).filter(dbmodel.Users.phone_no == user.phone_no).first()
  if check_phone_no : 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Phone Number already in use")
  invoice= cryptochill_api_request(f'invoices/{check_user.id}', method='GET')
  if invoice['result']['status'] != 'confirmed':
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,detail=f"Payment not confirmed yet")
  user.transaction_id = check_user.id
  user.email = check_user.email
  user.transaction_link = invoice['result']['profile_id']
  print(invoice['result']['amount']['requested']['amount'])
  if invoice['result']['amount']['requested']['amount'] == '1':
    user.capital = 25000
  if invoice['result']['amount']['requested']['amount'] == "270":
    user.capital = 50000
  if invoice['result']['amount']['requested']['amount'] == "470":
    user.capital = 100000
  if invoice['result']['amount']['requested']['amount'] == "850":
    user.capital = 200000
  custom_id = generate_custom_id("FR", 5)
  new_account = dbmodel.Users(id=custom_id, **user.dict())
  db.add(new_account)
  db.commit()
  db.refresh(new_account)
  await account_purchased("Registration Successful", user.email, {
    "title": "Account Purchase Successful",
    "name": user.first_name,
    "account": user.capital,
    "id": new_account.id
  })
  return  new_account




"""
User route
To load signed in user details
"""
@router.get('/current_user/me', response_model=user.UserOut)
async def get_current_user(db: Session = Depends(get_db),current_user: user.UserOut = Depends(oauth.get_current_user)):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with the given search criteria")
  return current_user






"""
User route
To reset users password
"""
@router.post('/password')
async def password_rest(email: user.passwordRest, db: Session = Depends(get_db)):
  email_exist= db.query(dbmodel.Users).filter(dbmodel.Users.email == email.email).first()
  if email_exist is not None :
    token = oauth.create_access_token(data={"user_id": email_exist.id, "email": email_exist.email})
    reset_link = f"https://myfundr.co/password/{token}"
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

"""
User route
To change user's password from profile
"""

@router.put('/change_password')
async def update_user_password(details:user.ChangePassword,db: Session = Depends(get_db),current_user: user.UserOut = Depends(oauth.get_current_user)):
  check_user = db.query(dbmodel.Users).filter(dbmodel.Users.id == current_user.id).first()
  check_password= utilis.verify(details.current_password,current_user.password)
  if not check_password:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"current password not a match")
  hash_new_password= utilis.hash(details.new_password)
  user_update= db.query(dbmodel.Users).filter(dbmodel.Users.id == current_user.id)
  user_update.update({"password": hash_new_password},synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_202_ACCEPTED)


"""
Payouts 
"""


