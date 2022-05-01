import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI

from .import models
from . database import engine

from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
  conn = psycopg2.connect(user='postgres', password='$%(muchori97)', host='db.dcwjrqbghffburtaocxi.supabase.co', port='5432', 
  database='postgres', cursor_factory=RealDictCursor)
  cursor = conn.cursor()
except Exception as error:
  print("Connect to a database: ", error)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

