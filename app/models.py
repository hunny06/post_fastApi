from .database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    user = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()"))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False, primary_key=True)