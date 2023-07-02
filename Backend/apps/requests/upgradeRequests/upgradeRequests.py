import warnings
from fastapi import  Depends,HTTPException,status,APIRouter,Response
from schemas.requests.upgrade import UpgradeRequest, UpgradeRequestOut, UpgradeStatus, UpgradeReject,UpgradeUpdate
from utlis.users.email import upgrade_request_completed, upgrade_request_rejected,upgrade_request,upgrade_request_processing
from models import dbmodel
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import desc 
from apps.users.oauth import get_current_user
from apps.admin.oauth import get_current_user_admin_login
from apps.requests.webSocket.ws import send_websocket_message

warnings.filterwarnings("ignore")


router = APIRouter(
    tags=["Upgrade Request"]
)



"""
User route
To send a upgarde request
"""
@router.post('/upgrade',status_code=status.HTTP_201_CREATED, response_model=UpgradeRequestOut)
async def send_upgrade_request(request: UpgradeRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id).first()
    if account_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} does not exist")
    if request.upgrade_to == account_details.phase :
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot upgrade to current phase")
    if account_details.status_upgrade == "Pending" or account_details.status_upgrade == "Sent":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot send multiple requests")
    request.first_name = account_details.first_name
    request.last_name = account_details.last_name
    request.email = account_details.email
    request.country = account_details.country
    request.analytics = account_details.analytics
    request.phone_no = account_details.phone_no
    request.role = account_details.role
    request.capital = account_details.capital
    request.status_upgrade = "Received"
    account_status = db.query(dbmodel.Users).filter(dbmodel.Users.id == request.id)
    account_status.update({"status_upgrade":"Sent","upgrade_to":request.upgrade_to})
    new_request = dbmodel.Requests(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    await upgrade_request("Upgrade Request Received!", account_details.email, {
    "title": "Upgrade Request Received!",
    "name": account_details.first_name,
    "phase": account_details.phase,
    "upgradeTo": request.upgrade_to
  })
    return  new_request





"""
Admin route
To update a upgarde request
"""
@router.put('/admin/upgrade/status')
async def update_upgrade_status(account:UpgradeStatus, db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if account_details == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status_upgrade":account.status_upgrade,"upgrading_reason":"N/A","upgrade_to":account.upgrade_to},synchronize_session=False)
  user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
  user_request.status_upgrade = account.status_upgrade
  db.commit()
  db.refresh(user_request)
  await upgrade_request_processing("Update! Upgrade Request Approved", account.email, {
    "title": "Update! Upgrade Request Approved",
    "name": account.first_name,
    "phase": account.current_phase,
    "upgradeTo": account.upgrade_to
  })
  return Response(status_code=status.HTTP_202_ACCEPTED)



"""
Admin route
To reject a upgarde request
"""
@router.put('/admin/upgrade/reject')
async def reject_upgrade_request(account:UpgradeReject,db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  check_account = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id).first()
  if check_account == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  if check_account.email != account.email:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Email not a match")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  account_details.update({"status_upgrade":"Rejected","upgrading_reason":account.reason,"upgrade_to":check_account.upgrade_to + "(failed)"},synchronize_session=False)
  user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
  user_request.status_upgrade = "Rejected"
  user_request.reason = account.reason
  db.commit()
  db.refresh(user_request)
  await upgrade_request_rejected(" Update! Upgrade Request Rejected", account.email, {
    "title": " Update! Upgrade Request Rejected",
    "name": check_account.last_name,
    "reason": account.reason,
    "phase": check_account.phase,
    "upgradeTo": check_account.upgrade_to
  })
  message = f"Your upgrade request to {account.phase} has been rejected!"
  user_id = str(account_details.first().id)
  await send_websocket_message(user_id, message)

  return Response(status_code=status.HTTP_208_ALREADY_REPORTED)



"""
Admin route
To confirm a upgarde request
"""
@router.put('/admin/upgrade/confirm')
async def confirm_upgrade_request(account: UpgradeUpdate , db: Session = Depends(get_db),current_user: int = Depends(get_current_user_admin_login)):
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
  if account_details.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {account.id} does not exist")
  account_details = db.query(dbmodel.Users).filter(dbmodel.Users.id == account.id)
 
  if account_details.first().status_upgrade == "Rejected":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has been rejected")
  elif account_details.first().status_upgrade == "Sent":
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {account.id} request has not been processed")
  else:
    account_details.update({"status_upgrade":"Completed","phase":account.phase,"upgrading_reason":"N/A"},synchronize_session=False)
    user_request = db.query(dbmodel.Requests).filter(dbmodel.Requests.id == account.id).order_by(desc(dbmodel.Requests.created_at)).limit(10).first()
    user_request.status_upgrade = "Confirmed"
    db.commit()
    await upgrade_request_completed("Update! Upgrade Request Completed", account_details.first().email, {
    "title": "Update! Upgrade Request Completed",
    "name":  account_details.first().last_name,
    "phase": account.phase,
    "type": account_details.first().type_meta,
    "account_id": account_details.first().account_id_meta,
    "mt_password": account_details.first().metatrader_password,
    "server": account_details.first().mt_server
    })
    message = f"Your upgrade request to {account.phase} has been approved!"
    user_id = str(account_details.first().id)
    await send_websocket_message(user_id, message)
    
  return Response(status_code=status.HTTP_202_ACCEPTED)

