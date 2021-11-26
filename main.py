from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to my Api"}

@app.get("/posts")
def get_post():
    return {"Data": "This is our post"}

@app.post("/create-post")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}     

