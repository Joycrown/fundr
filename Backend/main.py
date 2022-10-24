from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import dbmodel
from config.database import engine, get_db
from sqlalchemy.orm import Session 
from apps.users import main, auth, oauth
# from config.enivron import settings

# dbmodel.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)
app.include_router(auth.router)

@app.get("/")
def root():
  return{"message":"Hello World"}


@app.get('/testing')
def test_db(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
  user= db.query(dbmodel.Users).all()
  return current_user


