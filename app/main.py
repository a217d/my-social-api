from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user,auth, votes
from .config import settings
# يضمن عند بدء تشغيل السرفر الذهاب مباشره للقاعده البيانات للتاكد من وجود كافه الجداول
models.Base.metadata.create_all(bind = engine)

app = FastAPI()
     
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

