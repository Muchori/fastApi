import string
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[str] = None

try:
  conn = psycopg2.connect(user='postgres', password='$%(muchori97)', host='db.dcwjrqbghffburtaocxi.supabase.co', port='5432', 
  database='postgres', cursor_factory=RealDictCursor)
  cursor = conn.cursor()
except Exception as error:
  print("Connect to a database: ", error)


@app.get("/posts")
def get_post():
  posts = cursor.execute(""" SELECT * FROM posts """)
  cursor.fetchall()
  return {"data": posts}


@app.post("/posts/create", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
  cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING 
  * """,   
                  (post.title, post.content, post.published))
  new_post = cursor.fetchone()
  conn.commit()
  
  return {
    "data": new_post
  }   
 

@app.get("/posts/{id}")
def get_post(id):
  cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
  post = cursor.fetchone() 
  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found")

  return {
    "status": "success",
    "data": post
  }


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id):   
  cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (id,)) 
  delete_post = cursor.fetchone()
  conn.commit()  

  if delete_post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} not found" )

  return Response (status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/update/{id}")
def update_post(id, post: Post):

  cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING * """, 
  (post.title, post.content, post.published, (id),))
  updated_post= cursor.fetchone()
  conn.commit()

  if updated_post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )    
  
  return {
    'status':'success',
    'data': updated_post
  }
