from fastapi import  Depends,HTTPException,status,APIRouter,Response
from schemas.requests.payout import PayoutRequest, PayoutReject, PayoutConfirm, PayoutOut
from utlis.users.email import send_mail, rejected_payment_email
from models import dbmodel
from fastapi_pagination import Page, paginate
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import desc 
from utlis.users.email import send_mail
from apps.users import oauth
from apps.admin import oauth



router = APIRouter(
    tags=["Payout Request"]
)



"""
Users route
To request a payout
"""
@router.post('/payout',status_code=status.HTTP_201_CREATED)
async def payout_request(request: PayoutRequest, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id).first()
    if account_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} does not exist")
    request.status = "Pending"
    request.email= account_details.email
    request.analytics = account_details.analytics
    new_request = dbmodel.Payouts(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return  new_request



"""
Admin route
To reject a payout
"""
@router.put('/payout/reject')
async def reject_payout_request(account:PayoutReject,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  if check_account.email != account.email:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  user_request = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == account.id).order_by(desc(dbmodel.Payouts.created_at)).limit(10).first()
  user_request.status = "Rejected"
  user_request.reason = account.reason
  db.commit()
  db.refresh(user_request)
  await rejected_payment_email("payout Rejected", account.email, {
    "title": "payout Rejected",
    "name": check_account.last_name,
    "reason": account.reason
  })

  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)



"""
Admin route
To confirm/accept a payout
"""
@router.put('/payout/confirm')
async def confirm_payout_request(account: PayoutConfirm , db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  payout_details = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == account.id).order_by(desc(dbmodel.Payouts.created_at)).limit(10)
  if payout_details.first().status == "Rejected":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has been rejected")
  else:
    payout_details.first().status = "completed"
    payout_details.first().profit_share = account.profit_split
    
    
    db.commit()
    await send_mail("Payment Confirmed", account_details.first().email, {
    "title": "Payment Confirmed",
    "name":  account_details.first().last_name,
    })
    
    
  return Response(status_code=status.HTTP_202_ACCEPTED)

"""
User route
To request a payout history
"""
@router.get('/payout/{id}', response_model=Page[PayoutOut])
async def get_payout_history(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  account_payout_history = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No payout history for id: {id} yet")
  return paginate(account_payout_history)