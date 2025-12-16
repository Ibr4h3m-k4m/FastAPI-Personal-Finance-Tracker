

"""
Test configuration and fixtures for Personal Finance Tracker API.

This module provides shared pytest fixtures for testing:
- test_db: In-memory SQLite database for isolated tests
- client: FastAPI test client with database override
- test_user_data: Sample user credentials
- authenticated_client: Pre-authenticated client for protected endpoints
"""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.user import User
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient




@pytest.fixture
def test_db():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use static pool for in-memory DB
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    """Create a FastAPI test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
        
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user_data():
    """Provide reusable test user credentials."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }


@pytest.fixture()
def authenticated_client(client, test_user_data):
    """Create authenticated client for testing protected endpoints."""
    client.post("/api/v1/auth/register", json=test_user_data)
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client