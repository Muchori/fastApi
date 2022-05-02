from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[str] = None

class PostCreate(PostBase):
  pass

class UserResponse(BaseModel):
  id: str
  email: EmailStr
  created_at: datetime
  class Config:
    orm_mode = True

class PostResponse(PostBase):
  id: str
  created_at: datetime
  owner_id: str
  owner: UserResponse ## returns a pydantic type response in post response
  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str
  class Config:
    orm_mode = True

class Token(BaseModel):
  access_token: str
  token_type: str

class TokeData(BaseModel):
  id: Optional[str] = None

