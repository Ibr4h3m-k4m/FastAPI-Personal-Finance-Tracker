



def test_create_transaction(authenticated_client,test_transaction_data):
    """Test creating valid transactions(income and expense)"""
    # Create expense transaction
    response = authenticated_client.post("/api/v1/transactions/", json=test_transaction_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == test_transaction_data["amount"]
    assert data["category"] == test_transaction_data["category"]
    assert data["type"] == test_transaction_data["type"]
    
    # Create income transaction
    income_data = test_transaction_data.copy()
    income_data["type"] = "income"
    income_data["amount"] = 200.0
    response = authenticated_client.post("/api/v1/transactions/", json=income_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == income_data["amount"]
    assert data["category"] == income_data["category"]
    assert data["type"] == income_data["type"]
    
    #Testing without authentication
    
    