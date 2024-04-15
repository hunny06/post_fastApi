from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password):
    return pwd_context.hash(password)

def validate(raw_password, hashed_password):
    return pwd_context.verify(raw_password,hashed_password)
