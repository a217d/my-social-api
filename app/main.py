from typing import Optional # استدعاء مكتبة Optional من typing
from fastapi import Body, FastAPI,HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
import psycopg2 # call liblary con with Postgre sql
from psycopg2.extras import RealDictCursor # مكتبه تجعل نتائج الاستعلام ع شكل قواميس
import time

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

    

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# search with id 
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# search with id deleted 
def find_index_posts(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
        

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# create a post status code 201 means created
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # this qury more securty
    cursor.execute(
        """ INSERT INTO posts(titlle,content, published)  VALUES (%s, %s,%s) returning *""", 
                    (post.title,post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit() # save the chenge in db 
    
    return {"data": new_post}


# get latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {
        "latest_post": post
    }

# get id of post
@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    one_post = cursor.fetchone()
    if not one_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} was not found")
    
    return {
        "post_detail": one_post
    }


# update of posts
@app.put("/update/posts/{id}")
def update_posts(id: int, post: Post):
    index = find_index_posts(id)
    if index == None:
            # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")
    
    post_dict = post.dict() # يقوم بتحويل البيانات التي تم استلامها الى قاموس
    post_dict["id"] = id
    my_posts[index] = post_dict

    return{"massege": post_dict}


@app.delete("/delete/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting posts
    # 
    index = find_index_posts(id)
    if index == None:
        # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
