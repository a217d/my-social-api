from pydantic import BaseModel,EmailStr #مكتبه تحدد كيفيه هيكل البيانات المطلوبه
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# لحصر البيانات التي يتم ارجاعها للمستخدم 
class Post(PostBase):
    id: int
    created_at: datetime


# Recust كلاس الطلبات
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# كلاس الاستجابه Respouns
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# التحقق من صحه البيانات المدخله
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response (استجابة)
class Token(BaseModel):
    access_token: str
    token_type: str

# أداة داخلية لحمل البيانات التي نستخرجها من التوكن بعد فك تشفيره
class Tokendata(BaseModel):
    id : Optional["str"] = None



