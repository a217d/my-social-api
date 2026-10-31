from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #created sessionmaker
from psycopg2.extras import RealDictCursor # مكتبه تجعل نتائج الاستعلام ع شكل قواميس
import psycopg2 # call liblary con with Postgre sql
import time


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

# while True:
# # create call with db
#     try:
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='fastapi', 
#             user='postgres', 
#             password='123456789', 
#             cursor_factory=RealDictCursor # داله ترجع الاستعلام ع شكل dict()
#         )
#         cursor = conn.cursor() #داله تنفيذ الاولمر بداخل db
#         print("database connection was successfull!")
#         break

#     except Exception as error:
#         print("connecting to database failed")
#         print("Error:" ,error)
#         time.sleep(2)