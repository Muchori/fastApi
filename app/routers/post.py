from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter


from typing import List, Optional

from ..import models, schemas, oauth2

from ..database import get_db



router = APIRouter(
  prefix= "/posts",
  tags= ['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_post(
  db: Session = Depends(get_db), 
  current_user: str = Depends(oauth2.get_current_user), 
  limit: int = 10, 
  skip: int = 0,
  search: Optional[str] = ""):

  ## 
  # querying post py filter using limit, 
  # search using the title string and 
  # skip for pagination
  # 
  # ##
  posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  ## getting post fr current logged in user
  ##posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
  # posts = cursor.execute(""" SELECT * FROM posts """)
  # cursor.fetchall()
  # return {"data": posts}
  return posts

@router.post("/create", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
  post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  current_user: str = Depends(oauth2.get_current_user)):

  new_post = models.Post(
    owner_id = current_user.id,
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
def get_one_post(id, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

  ## querying the post of the current logged in user
  post = db.query(models.Post).filter(models.Post.id == id).first()
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
  # post = cursor.fetchone() 
  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found")

  ## querying one post with id of logged in user
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform the action")

  return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (id,)) 
  # delete_post = cursor.fetchone()
  # conn.commit()  
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found" )

  ## deleting post with id of logged in user
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform the action")

  post_query.delete(synchronize_session=False)
  db.commit() 

  return {
    "status": "success",
  }

@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(
  id, updated_post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  current_user: str = Depends(oauth2.get_current_user)):
  # cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING * """, 
  # (post.title, post.content, post.published, (id),))
  # updated_post= cursor.fetchone()
  # conn.commit()

  ## quering post from db with id
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()  

  if post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" ) 
  
  ## updating post with id of logged in user
  if post.owner_id != current_user.id: ## 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform the action")
  
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()  

  return post_query.first()