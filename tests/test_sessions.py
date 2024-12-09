def test_user_auth_flow(test_client):
    response = test_client.post("/register", json={"username": "testuser", "password": "password"})
    assert response.status_code == 201

    response = test_client.post("/login", json={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json

    headers = {"Authorization": f"Bearer {response.json['access_token']}"}
    response = test_client.get("/profile", headers=headers)
    assert response.status_code == 200
