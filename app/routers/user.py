from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(
    prefix="/users", tags=["User"]
)

@router.post('/', response_model=schemas.UserPost)
def createUser(data: schemas.UserBase, db: Session = Depends(get_db)):
    data.password = utils.hash(data.password)
    new_user = models.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserPost)
def getUser(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Id is not found    ")
    
    return user