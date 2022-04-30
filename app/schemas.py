from datetime import datetime
import email
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[str] = None

class PostCreate(PostBase):
  pass


class PostResponse(PostBase):
  id: str
  created_at: datetime

  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str


class UserResponse(BaseModel):
  id: str
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True