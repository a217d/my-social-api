from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #created sessionmaker

#  رابط  الاتصال ب قاعده البيانات باستخدام الطريقه الكلاسيكيه 
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:123456789@localhost/fastapi' 

# إنشاء المحرك لاداره الاتصال مع السرفر
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# create class
Base = declarative_base()

def get_db():
    # فتح جلسه 
    db = SessionLocal() #الحصول ع جلسه مع قاعده البيانات 
    try:
        yield db 
    # اغلاق الجلسه لتنجنب استهلاك الموارد
    finally:
        db.close()