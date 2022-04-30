from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from typing import List

from ..import models, schemas
from ..database import get_db



router = APIRouter(
  prefix= "/posts",
  tags= ['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  # posts = cursor.execute(""" SELECT * FROM posts """)
  # cursor.fetchall()
  # return {"data": posts}
  return posts

@router.post("/create", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
  new_post = models.Post(
    **post.dict()
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING 
  # * """,   
  #                 (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # conn.commit()
  
  return  new_post  

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
  # post = cursor.fetchone() 
  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found")

  return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (id,)) 
  # delete_post = cursor.fetchone()
  # conn.commit()  
  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found" )

  post.delete(synchronize_session=False)
  db.commit() 

  return {
    "status": "success",
  }

@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(id, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
  # cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING * """, 
  # (post.title, post.content, post.published, (id),))
  # updated_post= cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()  

  if post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" ) 
  
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()  

  return post_query.first()