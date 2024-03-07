from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, HTTPException, Depends, APIRouter
from typing import Optional, List

from .. import schemas, models, oauth2
from ..database import get_db

routes = APIRouter(prefix="/posts", tags=['Users'])

@routes.get("/", response_model=List[schemas.PostOutput])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Star.post_id).label("stars")).join(models.Star, models.Star.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@routes.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    if new_post:
        return new_post
    else:
        return {"message": "No post created"}


@routes.get('/{id}', response_model=schemas.PostOutput)
def get_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Star.post_id).label("stars")).join(models.Star, models.Star.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    return post


@routes.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    current_post = post.first()

    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")

    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post.first()


@routes.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    current_post = post.first()

    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()