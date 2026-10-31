from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Text

from .database import Base # call the base class
class Post(Base):
    # create table
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'True', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True),
                        nullable= False,server_default="now()")
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False) # foreign key to user table


    owner = relationship("User") # to get the user data from the user table


class User(Base):
    # create table User
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True),
                             nullable= False,server_default="now()")
    
    