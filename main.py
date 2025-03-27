"""
FastAPI app to test config and database.
"""

import uvicorn
from fastapi import FastAPI
from app.core.config import settings  # Import our settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

@app.get("/test")
def test():
    """
    Simple endpoint to verify that the configuration and database connection work.
    """
    return {"message": "Configuration & database are set up!"}

if __name__ == "__main__":
    # Run the app with Uvicorn for local development
    uvicorn.run(app, host="0.0.0.0", port=8000)
