

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


def create_authenticated_client(user_data, test_db):
    """Helper to spawn a new client and log in a specific user."""
    new_client = TestClient(app)
    # Override DB for this specific client instance
    app.dependency_overrides[get_db] = lambda: test_db
    
    # Register and Login
    new_client.post("/api/v1/auth/register", json=user_data)
    response = new_client.post(
        "/api/v1/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]}
    )
    
    token = response.json()["access_token"]
    new_client.headers.update({"Authorization": f"Bearer {token}"})
    return new_client

@pytest.fixture
def authenticated_client(test_db, test_user_data):
    yield create_authenticated_client(test_user_data, test_db)

@pytest.fixture
def second_authenticated_client(test_db):
    user2_data = {
        "email": "other@example.com", 
        "username": "otheruser", 
        "password": "password123"
    }
    yield create_authenticated_client(user2_data, test_db)

@pytest.fixture()
def test_transaction_data():
    """"Provide Sample transaction data for creating transactions"""
    return {
        "amount": 100.0,
        "description": "Weekly grocery shopping",
        "transaction_type": "expense"
    }
    
@pytest.fixture()
def create_transaction():
    """"Helper function to create a transaction in the database"""
    def _create_transaction(db, user_id, transaction_data):
        from app.models.transaction import Transaction
        
        transaction = Transaction(
            user_id=user_id,
            amount=transaction_data["amount"],
            description=transaction_data.get("description"),
            transaction_type=transaction_data["transaction_type"],
            date=transaction_data.get("date") 
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    return _create_transaction

