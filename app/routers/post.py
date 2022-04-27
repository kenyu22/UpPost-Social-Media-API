from fastapi import Response, FastAPI, HTTPException, status, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .. import models, schemas, oauth2
from ..database import get_db
from ..config import settings

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

while True:
    try:
        conn = psycopg2.connect(host=f"{settings.database_hostname}", database=f"{settings.database_name}",
                                user=f"{settings.database_username}", password=f"{settings.database_password}", cursor_factory=RealDictCursor)  # gives column name and value
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as error:
        print("Connection to database failed.")
        print(f"Error: {error}")
        time.sleep(5)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM socialmedia """)
    # posts = cursor.fetchall()
    # return posts
    print(search)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    print(current_user.id)
    cursor.execute("""INSERT INTO socialmedia (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published, current_user.id))

    new_post = cursor.fetchone()
    # commits the change into our database
    conn.commit()
    return new_post
# title str, content str


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM socialmedia WHERE id = %s """, (str(id),))
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # if the post of the id is not found, updated status code to not found (404)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID:[{id}] was not found.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  #  cursor.execute(
    #     """ DELETE FROM socialmedia WHERE id = %s RETURNING * """, (str(id),))
  #  deleted_post = cursor.fetchone()
  #  conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID:[{id}] does not exist.")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    return response


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    # cursor.execute(""" UPDATE socialmedia SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post is None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f"The post with ID:[{id}] does not exist.")
    # if models.Post.id != current_user.id:
    #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail="Not authorized to perform requested action")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID:[{id}] does not exist.")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    # return updated_post
