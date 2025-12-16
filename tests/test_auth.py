

def test_register_duplicate_email(client,test_user_data):
    """Test registering with an email that's already taken"""
    #First sign up with this email
    client.post("/api/v1/auth/register", json=test_user_data)
    #Second attempt 
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert "email" in response.json()["detail"].lower()
    assert "used" in response.json()["detail"].lower()

def test_login_success_with_email(client,test_user_data):
    """Test Creating a new client and sign in"""
    client.post("/api/v1/auth/register", json=test_user_data)
    response = client.post("/api/v1/auth/login", data={"username": test_user_data["email"],
            "password": test_user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_update_to_taken_email(client,test_user_data):
    """Test updating to an email that's already taken"""
    # Register first user
    user1 = {
        "email": "user1@test.com",
        "username": "user1",  # ← Add username
        "password": "password123"
    }
    client.post("/api/v1/auth/register", json=user1)
    
    # Register second user and login as them
    user2 = {
        "email": "user2@test.com",
        "username": "user2",  # ← Add username
        "password": "password123"
    }
    client.post("/api/v1/auth/register", json=user2)
    #login with the second user
    login_response = client.post("/api/v1/auth/login",
        data={
            "username": user2["email"],
            "password": user2["password"]
        })
    token = login_response.json()["access_token"]
    # Set auth header with user2's token
    client.headers.update({"Authorization": f"Bearer {token}"})
    # Try to update user2's email to user1's email
    response = client.put(  # ← This is the response you check!
        "/api/v1/users/me",  # ← Correct endpoint
        json={"email": user1["email"]}
    )
    
    assert response.status_code == 400
    assert "already in use" in response.json()["detail"].lower()
    



def test_get_current_user(authenticated_client, test_user_data):
    """Test getting user profile works"""
    response = authenticated_client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == test_user_data["email"]
    
    
def test_get_user_no_token(client):
    """Test profile endpoint requires authentication"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_update_user_email(authenticated_client):
    """Test updating email"""
    response = authenticated_client.put("/api/v1/users/me", json={"email": "new@test.com"})
    
    assert response.status_code == 200
    assert response.json()["email"] == "new@test.com"

def test_delete_user(authenticated_client):
    """Test deleting account"""
    response = authenticated_client.delete("/api/v1/users/me")
    
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()