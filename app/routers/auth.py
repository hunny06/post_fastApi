from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .. database import get_db
from sqlalchemy.orm import Session
from .. import models, utils, oauth



router = APIRouter(prefix="/login", tags = ['Auth'])


@router.post('/')
def login(credentials : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    if not utils.validate(credentials.password, user.password):
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
    encode_jwt = oauth.create_token(data={"user_id":user.id})
    

    return {"token" : encode_jwt, "token_type": "bearer"}