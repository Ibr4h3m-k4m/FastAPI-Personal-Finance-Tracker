



def test_create_transaction(authenticated_client,test_transaction_data):
    """Test creating valid transactions(income and expense)"""
    # Create expense transaction
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    print(response.json()) 
    assert response.status_code == 201
    data = response.json()
    assert float(data["amount"]) == test_transaction_data["amount"]
    assert data["transaction_type"] == test_transaction_data["transaction_type"]
    
    # Create income transaction
    income_data = test_transaction_data.copy()
    income_data["transaction_type"] = "income"
    income_data["amount"] = 200.0
    response = authenticated_client.post("/api/v1/transactions/", json=income_data)
    assert response.status_code == 201
    data = response.json()
    assert float(data["amount"]) == income_data["amount"]  # Compare to income_data, not test_transaction_data
    assert data["transaction_type"] == income_data["transaction_type"]
        

#Testing with an empty description and custom date    
def test_create_transaction_no_description(authenticated_client,test_transaction_data):
    """Test Creating a transaction with no  description plus a custom date"""
    test_transaction_data["description"] = ""
    test_transaction_data["date"] = "2024-02-15"
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == ""
    assert "2024-02-15" in data["date"]

# Testing without authentication (should fail 401 http error)

def test_create_transaction_no_auth(client,test_transaction_data):
    """ Test creating a transaction without being authentificated"""
    response = client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 401
    

def test_create_transaction_invalid_amount(authenticated_client,test_transaction_data):
    """ Test creating a transaction with an invalid amount (negative)"""
    test_transaction_data["amount"] = -100
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 422
    assert "greater than 0" in response.json()["detail"][0]["msg"].lower()
    
    # Testing with Zero amount
    test_transaction_data["amount"] = 0
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 422
    assert "greater than 0" in response.json()["detail"][0]["msg"].lower()
    

from datetime import datetime, timedelta, timezone
def test_create_transaction_future_date(authenticated_client,test_transaction_data):
    """ Test creating a transaction with a date more than 30 days in the future"""
    # Calculate a date 31 days in the future
    future_date = (datetime.now(timezone.utc) + timedelta(days=31)).date()
    test_transaction_data["date"] = str(future_date)
    
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 422
    assert "30 days" in response.json()["detail"][0]["msg"].lower()

def test_list_transactions_empty(authenticated_client):
    """ Test Listing transactions of a user who has none (no transactions yet)"""
    response = authenticated_client.get("/api/v1/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    
def test_list_transactions_multiple(authenticated_client,create_transaction,test_transaction_data,test_db):
    """ Test Listing transactions when multiple transactions exist for the user"""
    user_id = 1 
    for i in range(3):
        authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    
    response = authenticated_client.get("/api/v1/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3  # Should return 3 transactions
    
    
def test_list_transactions_user_isolation(authenticated_client, second_authenticated_client, test_transaction_data):
    # User 1 creates a transaction and we capture the ID
    res1 = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user1_tx_id = res1.json()['id']
    
    # User 2 creates a transaction
    res2 = second_authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user2_tx_id = res2.json()['id']
    
    # User 1 lists transactions
    response_user1 = authenticated_client.get("/api/v1/transactions/")
    data_user1 = response_user1.json()
    
    # ASSERTIONS:
    # 1. Check that User 1 sees their own ID
    assert any(tx['id'] == user1_tx_id for tx in data_user1)
    # 2. Check that User 1 DOES NOT see User 2's ID (Strict Isolation)
    assert all(tx['id'] != user2_tx_id for tx in data_user1)
    
    
def test_get_transaction_not_found(authenticated_client):
    """ Test getting a transaction that does not exist"""
    response = authenticated_client.get("/api/v1/transactions/9999",)
    assert response.status_code == 404


def test_get_transaction_other_user(authenticated_client, second_authenticated_client, test_transaction_data):
    """ Test getting a transaction that belongs to another user"""
    # User 1 creates a transaction
    res1 = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user1_tx_id = res1.json()['id']
    
    # User 2 creates a transaction
    res2 = second_authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user2_tx_id = res2.json()['id']
    
    # User 1 tries to get User 2's transaction
    response = authenticated_client.get(f"/api/v1/transactions/{user2_tx_id}")
    assert response.status_code == 404

def test_delete_transaction(authenticated_client, test_transaction_data):
    """ Test deleting a transaction that belongs to the user"""
    # Create a transaction
    res1 = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user1_tx_id = res1.json()['id']
    
    # Delete the transaction
    response = authenticated_client.delete(f"/api/v1/transactions/{user1_tx_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = authenticated_client.get(f"/api/v1/transactions/{user1_tx_id}")
    assert get_response.status_code == 404 

def test_delete_transaction_not_found(authenticated_client):
    """ Test deleting a transaction that does not exist"""
    response = authenticated_client.delete("/api/v1/transactions/9999")
    assert response.status_code == 404

def test_delete_transaction_other_user(authenticated_client, second_authenticated_client, test_transaction_data):
    """ Test deletting a transaction that belongs to another user"""
    # User 1 creates a transaction
    res1 = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    user1_tx_id = res1.json()['id']
    
    # User 2 tries to delete User 1's transaction
    response = second_authenticated_client.delete(f"/api/v1/transactions/{user1_tx_id}")
    assert response.status_code == 404  
    