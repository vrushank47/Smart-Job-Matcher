from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.routes import router as api_router
from app.services.matcher import analyze  # your real module name
print(analyze(
    "Graphic designer experienced with Photoshop, Illustrator and UI design.",
    "We are looking for a Python developer experienced with FastAPI, REST APIs, MongoDB and Git.",
))

app = FastAPI(
    title="Smart Job Matcher API",
    description="Backend API for Smart Job Matcher service",
    version="0.1.0",
)

# Enable CORS for development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount feature routers
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Job Matcher API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
