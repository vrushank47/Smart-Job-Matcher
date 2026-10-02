from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router

app = FastAPI(
    title="Smart Job Matcher API",
    description="Backend API for Smart Job Matcher service",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Job Matcher API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}