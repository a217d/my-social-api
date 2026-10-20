from typing import Optional # استدعاء مكتبة Optional من typing

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    print(post.rating)
    print(post.dict())
    return {"data": post}

@app.post("/posts{id}")
def create_post(post: Post,id: int):
    if id in my_posts:
        return {"data": post}