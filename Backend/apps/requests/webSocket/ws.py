from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.responses import HTMLResponse
from typing import Dict
from websockets.exceptions import ConnectionClosedError


router= APIRouter(
    tags=["websocket"]
)

# Store the connected WebSocket clients
websocket_clients: Dict[str, WebSocket] = {}


async def send_websocket_message(user_id: str, message: str):
    print(websocket_clients)
    if user_id in websocket_clients:
        websocket = websocket_clients[user_id]
        await websocket.send_text(message)



# WebSocket endpoint
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()
    websocket_clients[user_id] = websocket
    
    try:
        while True:
            # Wait for messages from WebSocket clients, if needed
            data = await websocket.receive_text()
            print(f"Received message from user {user_id}: {data}")
            print("alright")
    except ConnectionClosedError:
        # Handle disconnection
        del websocket_clients[user_id]
        print(f"User {user_id} disconnected")

# Approve user request endpoint
@router.post("/approve-request/{user_id}")
async def approve_request(user_id: str):
    # print(websocket_clients)
    # Perform the logic to approve the user's request here
    
    # Check if the user's WebSocket connection exists
    if user_id in websocket_clients:
        websocket = websocket_clients[user_id]
        print(websocket_clients[user_id])
        await websocket.send_text("Your request has been approved!")
