from fastapi import FastAPI

from . import models
from .database import engine
from .routes import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.routes)
app.include_router(post.routes)
app.include_router(auth.routes)

@app.get("/")
async def root():
    return {"message": "Hello World!!"}