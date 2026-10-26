from typing import Optional # استدعاء مكتبة Optional من typing
from fastapi import FastAPI,HTTPException, status, Response, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2 # call liblary con with Postgre sql
from psycopg2.extras import RealDictCursor # مكتبه تجعل نتائج الاستعلام ع شكل قواميس
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# يضمن عند بدء تشغيل السرفر الذهاب مباشره للقاعده البيانات للتاكد من وجود كافه الجداول
models.Base.metadata.create_all(bind = engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
# create call with db
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='123456789', 
            cursor_factory=RealDictCursor # داله ترجع الاستعلام ع شكل dict()
        )
        cursor = conn.cursor() #داله تنفيذ الاولمر بداخل db
        print("database connection was successfull!")
        break

    except Exception as error:
        print("connecting to database failed")
        print("Error:" ,error)
        time.sleep(2)
     
        

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return{"data": posts}



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}

# create a post status code 201 means created
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # this query withe sqlachemy
   
    new_post = models.Post(**post.dict())# تحويله الى قاموس بدلا من التمرير بشكل منفصل

    db.add(new_post)
    db.commit() # save the chenge in db
    db.refresh(new_post)# return the new post

    return {"data": new_post}

# get id of post
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # فلتره وجلب البيانات التي تحمل نفس قيمه id المدخل
    one_post =db.query(models.Post).filter(models.Post.id == id).first()
    
    if not one_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} was not found")
    
    return {
        "post_detail": one_post
    }


# update of posts
@app.put("/update/posts/{id}")
def update_posts(id: int, update_post: Post, db: Session = Depends(get_db)):

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    post = update_post_query.first()

    if post == None:
            # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")

    #if not null
    update_post_query.update(update_post.dict(), synchronize_session= False)

    db.commit()

    return{"massege": update_post_query.first()}


@app.delete("/delete/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting sqlachemy posts
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None: # في حال لم يتم ارجاع بيانات
        # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")

    deleted_post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
