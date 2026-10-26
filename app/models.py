from sqlalchemy import Column, Integer, String, Boolean
from .database import Base # call the base class

class Post(Base):
    # create table
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, default= True, nullable= False)
    