from jose import JOSEError,jwt
from datetime import datetime, timedelta, timezone

# secry_key
# algorithm
# expriation time 

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