def test_login_with_demo_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@oceanguard.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "access_token" in data
    assert "refresh_token" in data


def test_register_and_get_me(client):
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@oceanguard.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
        },
    )
    assert register.status_code == 200

    tokens = register.json()["data"]
    auth_header = "Bearer " + tokens["access_token"]
    me = client.get("/api/v1/users/me", headers={"Authorization": auth_header})
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "newuser@oceanguard.com"
