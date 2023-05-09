from fastapi import  Depends,HTTPException,status,APIRouter,Response, Query
from config.environ import settings
from models import dbmodel
from apps.cyptochil.cryptochilSignUp import create_access_token
from config.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import or_
from utlis.users.email import account_purchased, password_rest_email
from schemas.users import user
from typing import Optional
import time
import base64
import hashlib
import hmac
import json
import requests


router= APIRouter(
    tags=["Cyptochil"]
)





def encode_hmac(key, msg, digestmod=hashlib.sha256):
    return hmac.new(key.encode(), msg=msg, digestmod=digestmod).hexdigest()

def cryptochill_api_request(endpoint, payload=None, method='POST'):
    payload_nonce = str(int(time.time() * 1000))
    request_path = '/v1/%s/' % endpoint
    payload = payload or {}
    payload.update({'request': request_path, 'nonce': payload_nonce})

    # Encode payload to base64 format and create signature using your API_SECRET 
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = encode_hmac(settings.api_secret_key, b64)

    # Add your API key, encoded payload and signature to following headers
    request_headers = {
        'X-CC-KEY': settings.api_key,
        'X-CC-PAYLOAD': b64,
        'X-CC-SIGNATURE': signature,
    }

    # Make request
    response = requests.request(method, settings.api_url + request_path, headers=request_headers)
    return response.json()

async def cryptochil_database(id:str, email:str, amount:str, profile_id:str, db:Session=Depends(get_db)):
    # print(email)
    check_email = db.query(dbmodel.Cryptochil).filter(dbmodel.Cryptochil.email == email).first()
    if check_email : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
    new_account = dbmodel.Cryptochil(transaction_id=id, email=email, amount=amount, profile_id=profile_id)
    create_token= create_access_token(data={"transaction_id": id, "email": email})
    signup_link = f"https://myfundr.co/signup/{create_token}"
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    await password_rest_email("Registration Successful", email,{
      "title": "Account Purchase Successful",
      "name": email,
      "reset_link": signup_link
    })

    return  new_account


@router.post("/cryptochill/{endpoint}")
async def cryptochill(endpoint: str, payload: Optional[dict] = None, method: str = 'POST',db: Session = Depends(get_db)):
    try:
        response = cryptochill_api_request(endpoint, payload, method)
        if response['result'] == 'error':
            # Handle the error here
            # print("API error:", response['message'])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" API error: {response['message']}")
            # return {"result": "error", "message": response['message']}
        else:
            new_account = await cryptochil_database(response['result']['id'], response['result']['passthrough']['email'],response['result']['amount']['requested']['amount'],response['result']['profile_id'], db)
            # print(new_account)
            # Process the successful response
            return response
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print("Request failed:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" Request failed: {'connection error'}")
        # return {"result": "error", "message": str(e)}
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print("JSON decoding failed:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" JSON decoding failed: {'connection error'}")
        # return {"result": "error", "message": str(e)}