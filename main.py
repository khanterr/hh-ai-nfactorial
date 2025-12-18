from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models
from routers import jobs, companies

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Search Platform API",
    description="A comprehensive job search platform backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
app.include_router(companies.router, prefix="/api/v1", tags=["companies"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Search Platform API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)