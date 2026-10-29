from jose import JOSEError,jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# تحديد نقطة نهاية تسجيل الدخول (Login URL) للبحث عن التوكن تلقائياً في طلبات المستخدم
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# secry_key
# algorithm
# expriation time للتوكن

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# انشاء توكن
def create_access_token(data: dict):
    to_encode= data.copy()

    # تاريخ انتهاء صلاحيه التوكن 
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})# تحديث التوكن كل 30 دقيقه 

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# داله فك التشفير لتحقق من صحه التوكن
def verify_access_token(token: str, credentials_excption):
    try:
        # أ: محاولة فك التوكن باستخدام المفتاح السري والخوارزمية
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 1: استخراج الـ id من داخل الـ Payload
        id: str = payload.get("user_id") 

        # 2: التأكد أن الـ id فعلاً موجود وليست فارغة
        if id is None:
            raise credentials_excption # اطرده فوراً
        
        token_data = schemas.TokenData(id = id) 
    
    except JOSEError:
        # 3: إذا حدث أي خطأ في الفك (مثل انتهاء الوقت أو تزوير التوكن)
        raise credentials_excption # اطرده فوراً

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    # 1. نجهز رسالة الطرد (في حال فشل التحقق)
    credentials_excption = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentilas", 
        headers={"WWW-Authenticate": "Bearer"})

    # 2. نرسل التوكن ورسالة الطرد إلى دالة الفحص
    return verify_access_token(token, credentials_excption)