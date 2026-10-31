from fastapi import FastAPI,HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags = ['Posts'] # تقسم الصفحه حسب العنوان
)

@router.get("/", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends
            (oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "" ):

    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # جلب جميع البيانات من جدول posts
    return  posts

# create a post status code 201 means created
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends
            (oauth2.get_current_user)):

    # this query withe sqlachemy
    new_post = models.Post(owner_id= current_user.id, **post.dict())# تحويله الى قاموس بدلا من التمرير بشكل منفصل
    db.add(new_post)
    db.commit() # save the chenge in db
    db.refresh(new_post)# return the new post

    return  new_post

# get id of post
@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends
            (oauth2.get_current_user)):
    # فلتره وجلب البيانات التي تحمل نفس قيمه id المدخل
    one_post =db.query(models.Post).filter(models.Post.id == id).first()
    
    if not one_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} was not found")
    
    return one_post



# update of posts
@router.put("/{id}", response_model= schemas.Post)
def update_posts(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends
            (oauth2.get_current_user)):

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    post = update_post_query.first()

    if post == None:
            # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")

    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail= f"Not authorized to perform requested action")

    #if not null
    update_post_query.update(update_post.dict(), synchronize_session= False)

    db.commit()

    return update_post_query.first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends
            (oauth2.get_current_user)):
    # deleting sqlachemy posts
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    post = deleted_post.first() # جلب اول عنصر من البيانات التي تم جلبها

    if post == None: # في حال لم يتم ارجاع بيانات
        # رساله تظهر في حال عدم تطابق ال id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} does not exits")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform requested action")

    deleted_post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)