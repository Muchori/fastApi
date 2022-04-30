
import email
from enum import unique
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
import uuid

#generating unique uuid function
def generate_uuid():
    return str(uuid.uuid4())

class Post(Base):
  __tablename__ = "posts"

  id = Column(String, primary_key=True, nullable = False, default=generate_uuid)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default="TRUE", nullable=False)
  rating = Column(Integer, nullable=True)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))



class User(Base):
  __tablename__ = "users"

  id = Column(String, primary_key=True, nullable = False, default=generate_uuid)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=True)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))