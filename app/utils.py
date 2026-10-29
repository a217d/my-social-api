from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")# hasshing pass

# تشفير كلمه المرور
def hash(password: str):
    return pwd_context.hash(password)

# التحقق من صحه ادخال كلمه المرور 
def verify(plain_password, hashed_password):
    # المقارنه بين كلمه المرور المدخله والموجوده في db
    return pwd_context.verify(plain_password,hashed_password)