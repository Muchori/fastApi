from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .import models
from . database import engine
from . routers import post, user, auth, vote

## No longer needed if using alembic migrations
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# cors for security purpose
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "I dockerised the application"}

