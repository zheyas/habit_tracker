import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    response = client.post('/api/users/register/', {
        "email": "new@example.com",
        "username": "newuser",
        "password": "newpass123"
    })
    assert response.status_code == 201
    assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
def test_login_user():
    user = User.objects.create_user(email="login@test.com", username="loginuser", password="test123")
    client = APIClient()
    response = client.post('/api/users/login/', {
        "email": "login@test.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_login_with_wrong_credentials():
    client = APIClient()
    response = client.post('/api/users/login/', {
        "email": "wrong@test.com",
        "password": "nopass"
    })
    assert response.status_code == 401
