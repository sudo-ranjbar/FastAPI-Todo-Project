def test_login_response_401(anonymous_client):
    payload = {
        "email": "amhd.ranjbar@gmail.com",
        "password": "amh7711607"
    }
    response = anonymous_client.post("api/v1/users/login", json=payload)
    assert response.status_code == 401


def test_login_response_200(anonymous_client):
    payload = {
        "email": "test_email@gmail.com",
        "password": "123456"
    }
    response = anonymous_client.post("api/v1/users/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_register_response_201(anonymous_client):
    payload = {
        "username": "alihasan",
        "email": "ali@gmail.com",
        "password": "amh7711607",
        "confirm_password": "amh7711607"
    }
    response = anonymous_client.post("api/v1/users/register", json=payload)
    assert response.status_code == 201