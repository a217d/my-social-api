from typing import Optional, List # استدعاء مكتبة Optional من typing
from fastapi import FastAPI,HTTPException, status, Response, Depends
from pydantic import BaseModel 
from random import randrange
import psycopg2 # call liblary con with Postgre sql
from psycopg2.extras import RealDictCursor # مكتبه تجعل نتائج الاستعلام ع شكل قواميس
import time
from sqlalchemy.orm import Session 
from . import models, schemas,utils
from .database import engine, get_db
from .routers import post, user,auth


# يضمن عند بدء تشغيل السرفر الذهاب مباشره للقاعده البيانات للتاكد من وجود كافه الجداول
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

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
     

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

