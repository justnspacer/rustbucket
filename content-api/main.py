from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import content_blocks, search, keywords, media, user_roles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content_blocks.router)
app.include_router(search.router)
app.include_router(keywords.router)
app.include_router(media.router)
app.include_router(user_roles.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Content API"}