import pytest
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass',
        telegram_chat_id='123456789'
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email='another@example.com',
        username='another',
        password='anotherpass'
    )

@pytest.fixture
def pleasant_habit(user):
    return Habit.objects.create(
        user=user,
        place="диван",
        time="22:00",
        action="релакс",
        execution_time=60,
        periodicity=1,
        is_pleasant=True
    )