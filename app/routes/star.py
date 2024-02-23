from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


routes = APIRouter(
    prefix="/star",
    tags=['Stars']
)


@routes.post("/", status_code=status.HTTP_201_CREATED)
def star(star: schemas.Star, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == star.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {star.post_id} does not exist")

    star_query = db.query(models.Star).filter(models.Star.post_id == star.post_id, models.Star.user_id == current_user.id)

    found_star = star_query.first()
    if (star.dir == 1):
        if found_star:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already starred post with Id: {star.post_id}")
        new_star = models.Star(post_id=star.post_id, user_id=current_user.id)
        db.add(new_star)
        db.commit()
        return {"message": "successfully starred"}
    else:
        if not found_star:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already unstarred")

        star_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully unstarred"}