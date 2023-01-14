from fastapi import  Depends,HTTPException,status,APIRouter,Response
from schemas.requests.scale import ScaleRequest, ScaleRequestOut, ScaleStatus, ScaleReject,ScaleUpdate
from utlis.users.email import send_mail, rejected_payment_email
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import desc 
from utlis.users.email import send_mail
from apps.users import oauth
from apps.admin import oauth



router = APIRouter(
    tags=["Scale Request"]
)


"""
Users route
To request for scaling
"""
@router.post('/scale',status_code=status.HTTP_201_CREATED, response_model=ScaleRequestOut)
async def send_scale_request(request: ScaleRequest, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id).first()
    if account_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} does not exist")
    request.first_name = account_details.first_name
    request.last_name = account_details.last_name
    request.email = account_details.email
    request.country = account_details.country
    request.phone_no = account_details.phone_no
    request.role = account_details.role
    request.capital = account_details.capital
    request.status_scale = "Received"
    account_status = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id)
    account_status.update({"status_scale":"Sent","scale_to":request.scale_to})
    new_request = dbmodel.Requests(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return  new_request





"""
Admin route
To update a scale request
"""
@router.put('/scale/status')
async def update_scale_status(account:ScaleStatus, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status_scale":account.status,"scaling_reason":"N/A","scale_to":account.scale_to},synchronize_session=False)
  user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
  user_request.status_scale = account.status
  db.commit()
  db.refresh(user_request)
  return Response(status_code=status.HTTP_202_ACCEPTED)



"""
Admin route
To reject a scale request
"""
@router.put('/scale/reject')
async def reject_scale_request(account:ScaleReject,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  if check_account.email != account.email:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status_scale":"Rejected","scaling_reason":account.reason,"scale_to":check_account.scale_to + "(failed)"},synchronize_session=False)
  user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
  user_request.status_scale = "Rejected"
  user_request.reason = account.reason
  db.commit()
  db.refresh(user_request)
  await rejected_payment_email("Upgrade Rejected", account.email, {
    "title": "Upgrade Rejected",
    "name": check_account.last_name,
    "reason": account.reason
  })

  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)



"""
Admin route
To confirm a scale request
"""
@router.put('/scale/confirm')
async def confirm_scale_request(account: ScaleUpdate , db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first().status_scale == "Rejected":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has been rejected")
  if account_details.first().status_scale == "Sent":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has not been processed")
  account_details.update({"status_scale":"completed","capital":account.capital},synchronize_session=False)
  user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
  user_request.status_scale = "Confirmed"
  db.commit()
  await send_mail("Upgrade Successful", account_details.first().email, {
    "title": "Upgrade Successful",
    "name":  account_details.first().last_name,
    
    })
  return Response(status_code=status.HTTP_202_ACCEPTED)


