from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    security_key : str
    algorithm : str
    access_token_expire : int

    class Config():
        env_file = ".env"
settings = Setting()

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserPost(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime    


class PostsBase(BaseModel):
    title : str
    content : str
    published : Optional[bool] = False
    

class PostCreate(PostsBase):
    pass

class Post(PostsBase):
    id: int
    user_id : int
    user : UserPost
    
    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id : int
    vote_id : bool