from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import dbmodel
from config.database import  get_db
from sqlalchemy.orm import Session 
from apps.users import main, auth, oauth
from fastapi_pagination import add_pagination
from apps.requests.scaleRequests import scaleRequests
from apps.requests.upgradeRequests import upgradeRequests
from apps.requests.payoutRequests import payoutRequest
from apps.admin import admin


app = FastAPI()

origins= ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)
app.include_router(auth.router)
app.include_router(scaleRequests.router)
app.include_router(upgradeRequests.router)
app.include_router(payoutRequest.router)
app.include_router(admin.router)

add_pagination(app)

@app.get("/")
def root():
  return{"message":"Hello World"}


@app.get('/testing')
def test_db(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
  user= db.query(dbmodel.Users).all()
  return user


