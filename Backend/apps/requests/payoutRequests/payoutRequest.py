from fastapi import  Depends,HTTPException,status,APIRouter,Response,Query
from schemas.requests.payout import PayoutRequest, PayoutReject, PayoutConfirm, PayoutOut
from utlis.users.email import payout_request, payout_request_rejected, payout_request_processing, payout_request_confirmation
from models import dbmodel
from fastapi_pagination import Page, paginate
from config.database import get_db
from sqlalchemy import or_
from sqlalchemy.orm import Session 
from datetime import datetime
from sqlalchemy import desc 
from schemas.users import user
from apps.requests.webSocket.ws import send_websocket_message
from apps.users.oauth import get_current_user
from apps.admin.oauth import get_current_user_admin_login



router = APIRouter(
    tags=["Payout Request"]
)



"""
Users route
To request a payout
"""


@router.post('/payout',status_code=status.HTTP_201_CREATED, response_model=PayoutOut)
async def send_payout_request(request: PayoutRequest, db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id)
    if account_details.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} does not exist")
    if account_details.first().status_payout == "Pending" or account_details.first().status_payout == "Sent":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot send multiple requests")
    request.first_name = account_details.first().first_name
    request.last_name = account_details.first().last_name
    request.email = account_details.first().email
    request.analytics = account_details.first().analytics
    request.profit_share = account_details.first().profit_split
    request.payable_amount = request.amount * request.profit_share
    request.status = "Received"
    new_request = dbmodel.Payouts(**request.dict())
    account_details.update ({"status_payout":"Sent"},synchronize_session=False)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    await  payout_request("Payout Request Received!", request.email, {
    "title": "Payout Request Received!",
    "name": request.first_name,
    "amount": request.amount,
    "method": request.payment_method,
    "address": request.wallet_address
  })
    return  new_request



"""
Admin route
To reject a payout
"""
@router.put('/admin/payout/reject')
async def reject_payout_request(account:PayoutReject,db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  if check_account.email != account.email:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  user_request = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == account.id).order_by(desc(dbmodel.Payouts.created_at)).limit(10).first()
  user_request.status = "Rejected"
  user_request.reason = account.reason
  account_details.update ({"status_payout":"Rejected"},synchronize_session=False)
  db.commit()
  db.refresh(user_request)
  await payout_request_rejected ("Update! Payout Request Rejected", account.email, {
    "title": "Update! Payout Request Rejected",
    "name": account_details.first().first_name,
    "amount": user_request.amount,
    "reason": account.reason
  })
  message = f"Your payout request has been rejected!"
  user_id = str(account_details.first().id)
  await send_websocket_message(user_id, message)

  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)



"""
Admin route
To accept a payout
"""
@router.put('/admin/payout/pending')
async def accept_payout_request(account: PayoutConfirm , db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  payout_details = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == account.id).order_by(desc(dbmodel.Payouts.created_at)).limit(10)
  if payout_details.first().status == "Rejected":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has been rejected")
  else:
    payout_details.first().status = "Pending"
    # payout_details.first().profit_share = account.profit_split
    
    account_details.update ({"status_payout":"Pending"},synchronize_session=False)
    db.commit()
    await payout_request_processing("Update! Payout Request Approved", account_details.first().email, {
    "title": "Update! Payout Request Approved",
    "name": account_details.first().first_name,
    "amount":  account.amount_requested,
    "share":  account.payable_amount
    })
    
    
  return Response(status_code=status.HTTP_202_ACCEPTED)



"""
Admin route
To confirm a payout
"""
@router.put('/admin/payout/confirmed')
async def confirm_payout_request(account: PayoutConfirm , db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  payout_details = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == account.id).order_by(desc(dbmodel.Payouts.created_at)).limit(10)
  if payout_details.first().status != "Pending":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request hasnt been accepted")
  else:
    payout_details.first().status = "Completed"
    # payout_details.first().profit_share = account.profit_split
    account_details.update ({"status_payout":"Completed"},synchronize_session=False)
    
    db.commit()
    
    await  payout_request_confirmation("Update! Payout Request Completed", account.email, {
    "title": "Update! Payout Request Completed",
    "name": account_details.first().first_name,
    "share": payout_details.first().payable_amount,
    "amount": account.amount_requested,
    "method": account.payment_method,
    "address": account.wallet_address
  })
  message = f"Your payout request has been approved!"
  user_id = str(account_details.first().id)
  await send_websocket_message(user_id, message)
    
  return Response(status_code=status.HTTP_202_ACCEPTED)

"""
User route
To request a payout history
"""
@router.get('/payout/{id}', response_model=Page[PayoutOut])
async def get_payout_history(id: int, db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
  account_payout_history = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No payout history for id: {id} yet")
  return paginate(account_payout_history)




"""
Admin route
To get all payout request on fundr system
"""
@router.get("/payout/", response_model=Page[PayoutOut])
def get_all_payout(search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None),start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
    query = db.query(dbmodel.Payouts).order_by(dbmodel.Payouts.created_at)
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
User route
To get all payout request for current user
"""

@router.get('/history',response_model=Page[PayoutOut])
async def get_all_payout_for_current_user(db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
  check_history = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id==current_user.id).all()
  if not check_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No payout history for id: {id} yet")
  return paginate(check_history)


"""
Admin route
To get all received user payouts fundr 
"""
@router.get("/user/payouts/received", response_model=Page[PayoutOut])
async def get_all_users_payout_received( db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  users = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.status == "Received").all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payout Received Yet")
  return paginate(users)




"""
Admin route
To get all pending user payouts fundr 
"""
@router.get("/user/payouts/pending", response_model=Page[PayoutOut])
async def get_all_users_payout_pending( db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  users = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.status == "Pending").all()
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payout Accepted Yet")
  return paginate(users)




"""
Admin route
To get all completed user payouts fundr 
"""
@router.get("/user/payouts/completed", response_model=Page[PayoutOut])
async def get_all_users_payout_completed( search_query: str = Query(None, min_length=3, max_length=100),filter_query: str = Query(None), start_date: str = Query(None),
              end_date: str = Query(None), db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  query = db.query(dbmodel.Payouts).filter(or_(dbmodel.Payouts.status == "Completed", 
  dbmodel.Payouts.status == "Rejected"))
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
  if not users:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payout Completed Yet")
  return paginate(users)



"""
Admin route
To get a single payout request made by a user on fundr
"""
@router.get('/user/payout/serial_no/{id}',response_model=PayoutOut)
async def get_particular_payout_with_serial_no(id: str, serial_no:int, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_payout_history = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.id == id).all()
  if not account_payout_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No request history for id: {id} yet")
  payout = db.query(dbmodel.Payouts).filter(dbmodel.Payouts.serial_no == serial_no).first()
  if not payout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Payout Completed Yet")
  return payout
