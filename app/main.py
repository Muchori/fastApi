from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [{"title": "title of post 1", "contect": "content of post 1", "id" : 1}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] ==id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my Api"}



@app.get("/posts")
def get_post():
    return {"data": my_post}



@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    # print(post)
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_post.append(post_dict)
    return {"data": post_dict}   
 

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post {id} not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")

    return {"post_details": post}


# @app.get("/posts/latest")
# def get_latest_post():
#     post=my_post[len(my_post)-1]
#     return{"details": post}
    
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting a post
    #find the index in array that hass required ID
    #my post.pop (index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )

    my_post.pop(index)
    return Response (status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )
    
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {'data': post_dict}
