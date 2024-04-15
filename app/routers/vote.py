from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import database, schemas, models, oauth

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/")
def vote(data : schemas.Vote , db : Session = Depends(database.get_db), current_user:int = Depends(oauth.validate_user)):
    post_id = db.query(models.Post).filter(models.Post.id == data.post_id ).first()

    if not post_id:
        raise HTTPException(status_code=200,detail="Post id not found")

    query = db.query(models.Vote).filter(models.Vote.post_id == data.post_id, models.Vote.user_id == current_user.id)
    if data.vote_id:
        if query.first():
            raise HTTPException(status_code=400,detail="Alredy there")
        vote = models.Vote(user_id = current_user.id ,post_id = data.post_id)
        db.add(vote)
        db.commit()
        db.refresh(vote)    
    else:
        query.delete()
        db.commit()


    return {}