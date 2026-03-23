from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.scan import router

app = FastAPI()

# Updated CORS to allow more flexibility for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api") # Added prefix for better organization