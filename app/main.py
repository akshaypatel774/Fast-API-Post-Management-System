from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import post, user, auth, star


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.routes)
app.include_router(post.routes)
app.include_router(auth.routes)
app.include_router(star.routes)

@app.get("/")
def root():
    return {"message": "Hello World!!"}