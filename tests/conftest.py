import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine

@pytest.fixture(scope="function")
def client():
    """ 
    For each test function, we drop and recreate the database tables
    to ensure a clean state. 
    """

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    # Create a TestClient instance for sending HTTP requests to our app.
    with TestClient(app) as c:
        yield c
    
    # Optionally, drop the tables after each test run.
    Base.metadata.drop_all(engine)
