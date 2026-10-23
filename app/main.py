from typing import Optional # استدعاء مكتبة Optional من typing
from fastapi import Body, FastAPI,HTTPException, status, Response
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_posts(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
        

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

# create a post status code 201 means created
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# get latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {
        "latest_post": post
    }

# get id of post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail="post with id : {id} was not found")
    
    return {
        "post_detail": post
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
