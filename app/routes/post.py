from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, HTTPException, Depends, APIRouter
from typing import Optional, List

from .. import schemas, models, oauth2
from ..database import get_db

routes = APIRouter(prefix="/posts", tags=['Users'])

@routes.get("/", response_model=List[schemas.PostOutput])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # cur.execute(""" SELECT * FROM posts """)
    # posts = cur.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Star.post_id).label("stars")).join(models.Star, models.Star.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # User gets just his own posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts


@routes.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cur.fetchone()

    # conn.commit()
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    if new_post:
        return new_post
    else:
        return {"message": "No post created"}


@routes.get('/{id}', response_model=schemas.PostOutput)
async def get_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cur.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Star.post_id).label("stars")).join(models.Star, models.Star.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    return post


@routes.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cur.fetchone()

    # conn.commit()

    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")

    # return updated_post
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
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))

    # deleted_post = cur.fetchone()
    # conn.commit()
    
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")

    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    post = db.query(models.Post).filter(models.Post.id == id)

    current_post = post.first()

    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()



# @routes.get('/posts/latest')  Get Latest Post------------------------------------
# async def get_posts():
#     post = all_posts[len(all_posts) - 1]
#     return {"Post": post}


# def find_post(id: int):
#     for post in all_posts:
#         if post["id"] == id:
#             return post
#     return None

# def find_post_index(id: int):
#     for index, post in enumerate(all_posts):
#         if post["id"] == id:
#             return index
#     return None