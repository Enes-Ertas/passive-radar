from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.posts import router as posts_router

app = FastAPI()

# Next.js frontend'den veri çekebilmek için CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router, prefix="/posts")
