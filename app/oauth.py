from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session
from .schemas import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECURITY_CODE = settings.security_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now()  + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECURITY_CODE, algorithm = ALGORITHM)

    return encode_jwt

def validate_token(token:str, credential_validator):
    try:
        data = jwt.decode(token, SECURITY_CODE, algorithms = [ALGORITHM])
        if data["user_id"]:
            id =  data["user_id"]
            
    except JWTError as e:
        print(e)
        raise credential_validator
    return id

def validate_user(token:str = Depends(oauth2_schema),db:Session = Depends(database.get_db)):
    credential_validator = HTTPException(status_code=403,detail="token is not valid")
    id = validate_token(token, credential_validator)
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
