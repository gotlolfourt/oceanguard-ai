import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database.session import Base, engine
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


import pytest


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
