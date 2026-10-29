from pydantic import BaseModel,EmailStr #مكتبه تحدد كيفيه هيكل البيانات المطلوبه
from datetime import datetime


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