from fastapi import FastAPI,HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session

from app import database
from .. import models, schemas, oauth2

router = APIRouter(
    prefix= "/vote",
    tags = ['Votes'] # تقسم الصفحه حسب العنوان
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends 
         (oauth2.get_current_user)):
    
#   check if the post exist or not
    post =db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id : {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    fount_vote = vote_query.first()
    if (vote.dir == 1):
        if fount_vote:
            # رساله تظهر في حال وجود اعجاب سابق ع المنشور 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    # في حاله عدم وجود اعجاب سابق ع المنشور
    else:
        if not fount_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"vote does not exist")

        # في حاله وجود اعجاب سابق ع المنشور نقوم بحذفه
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
