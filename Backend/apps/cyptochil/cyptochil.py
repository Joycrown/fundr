from fastapi import  Depends,HTTPException,status,APIRouter,Response, Query
from config.environ import settings
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

@router.post("/cryptochill/{endpoint}")
async def cryptochill(endpoint: str, payload: Optional[dict] = None, method: str = 'POST'):
    try:
        response = cryptochill_api_request(endpoint, payload, method)
        if response['result'] == 'error':
            # Handle the error here
            print("API error:", response['message'])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" API error: {response['message']}")
            # return {"result": "error", "message": response['message']}
        else:
            # Process the successful response
            return response
        
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print("Request failed:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" Request failed: {str(e)}")
        # return {"result": "error", "message": str(e)}
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print("JSON decoding failed:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" JSON decoding failed: {str(e)}")
        # return {"result": "error", "message": str(e)}