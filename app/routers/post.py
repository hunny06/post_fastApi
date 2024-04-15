from sqlalchemy import func
from .. import models, schemas, oauth
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from ..database import get_db
from fastapi.params import Body
from typing import List
from random import randrange



router = APIRouter( prefix="/post", tags=["Posts"])


# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), get_current_user:int = Depends(oauth.validate_user), limit:int = 5, skip:int = 0, search:str= ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # post = cursor.fetchall()
    
    # post = db.query(models.Post).all()
    # print(post)
    # post = db.query(models.Post).filter(models.Post.user_id == get_current_user.id)
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(results)
    # for (post, votes) in results:
    #         print (post, votes)
    return results

@router.post('/oldpost')
def old_create_post(params : dict = Body ):
    print(params)
    return {"message": params["name"]}

@router.post('/', response_model=schemas.Post)
def createPost(params : schemas.PostCreate, db: Session = Depends(get_db), get_current_user:int = Depends(oauth.validate_user)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning *""",(params.title,params.content,params.published))
    # post = cursor.fetchone()
    # conn.commit()
    # user = oauth.validate_user()
    post = models.Post(user_id = get_current_user.id,**params.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    # new_post = params.model_dump()
    # new_post["id"] = randrange(0,10000000)
    # posts.routerend(new_post)
    return post

@router.get('/{id}', response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), get_current_user:int = Depends(oauth.validate_user)):

    # cursor.execute(""" SELECT * FROM posts where id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # post = [i for i in posts if i["id"] == id ]

    if not post:
        raise HTTPException(status_code=404, detail="Id is not found    ")
    
    if(post.user_id != get_current_user.id):
        raise HTTPException(status_code=404, detail="Invalid Access")

    return post

@router.delete('/{id}', response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), get_current_user:int = Depends(oauth.validate_user)):
    # cursor.execute(""" DELETE from posts where id = %s returning * """,(str(id)))
    # new_data = cursor.fetchone()
    # conn.commit()

    new_data = db.query(models.Post).filter(models.Post.id == id)

    # post = [i for i,k in  enumerate(posts) if k["id"] == id ]
    if not new_data:
        raise HTTPException(status_code=404, detail="Id is not found    ")
    # p = posts.pop(post[0])
    
    query = new_data.first()
    if(query.user_id != get_current_user.id):
        raise HTTPException(status_code=404, detail="Invalid Access")
    
    new_data.delete(synchronize_session = False)
    db.commit()
    return query

@router.put('/{id}', response_model=schemas.Post)
def update_post(id : int, data:schemas.PostCreate, db: Session = Depends(get_db),get_current_user:int = Depends(oauth.validate_user)):

    # cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s returning *""",(data.title, data.content, data.published, str(id)))
    # new_data = cursor.fetchone()
    # conn.commit()
    
    new_data = db.query(models.Post).filter(models.Post.id == id)
    
    
    data_o = new_data.first()

    if(data_o.user_id != get_current_user.id):
        raise HTTPException(status_code=404, detail="Invalid Access")
    
    if not data_o:
        raise HTTPException(status_code=404, detail="Id is not found    ")
    
    
    new_data.update(data.model_dump(), synchronize_session = False)
    db.commit()

    # post_index = [i for i,k in  enumerate(posts) if k["id"] == id ]
    # new_data = data.model_dump()
    # posts[post_index[0]]
    # new_data["id"] = id
    # posts[post_index[0]] = new_data  

    return data_o