"""
FastAPI app to test config and database.
"""

import uvicorn
from fastapi import FastAPI
from app.core.config import settings  # Import our settings
from app.db.database import Base, engine
from app.routers import exercises, auth, favorites, saves, ratings, collection, migrate

from fastapi.middleware.cors import CORSMiddleware

# Create all tables, including new models
Base.metadata.create_all(bind=engine)

# Intialize FastAPI app
app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

#Include router for: exercises, auth, favorites
app.include_router(exercises.router)
app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(saves.router)
app.include_router(ratings.router)
app.include_router(collection.router)
app.include_router(migrate.router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend ip address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    """
    Simple endpoint to verify that the configuration and database connection work.
    """
    return {"message": "Configuration & database are set up!"}

if __name__ == "__main__":
    # Run the app with Uvicorn for local development
    uvicorn.run(app, host="0.0.0.0", port=8000)
