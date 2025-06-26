import pytest
from habits.models import Habit
from unittest.mock import patch

# ----------------------------
# ✅ УСПЕШНОЕ СОЗДАНИЕ ПРИВЫЧКИ
# ----------------------------
@pytest.mark.django_db
@patch("habits.views.send_telegram_message.delay")
def test_create_valid_habit_successfully(mock_telegram, auth_client):
    """Создание привычки с валидными данными"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "08:00",
        "action": "чтение",
        "execution_time": 60,
        "periodicity": 1
    }, format='json')

    assert response.status_code == 201
    assert Habit.objects.count() == 1
    mock_telegram.assert_called_once()


# ----------------------------
# 🚫 ПРОВЕРКИ ВАЛИДАЦИИ (clean)
# ----------------------------

@pytest.mark.django_db
def test_validation_fails_if_execution_time_exceeds_120(auth_client):
    """Ошибка: время выполнения > 120 сек"""
    response = auth_client.post('/api/habits/', {
        "place": "офис",
        "time": "09:00",
        "action": "звонки",
        "execution_time": 130,
        "periodicity": 1
    }, format='json')

    assert response.status_code == 400
    assert "время выполнения" in str(response.data).lower()

@pytest.mark.django_db
def test_validation_fails_if_periodicity_exceeds_7(auth_client):
    """Ошибка: периодичность > 7"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "18:00",
        "action": "учёба",
        "execution_time": 60,
        "periodicity": 10
    }, format='json')

    assert response.status_code == 400
    assert "периодичность" in str(response.data).lower()

@pytest.mark.django_db
def test_validation_fails_if_reward_and_related_habit_given(auth_client, pleasant_habit):
    """Ошибка: одновременно reward и related_habit"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "10:00",
        "action": "учёба",
        "execution_time": 60,
        "periodicity": 1,
        "reward": "кофе",
        "related_habit": pleasant_habit.id
    }, format='json')

    assert response.status_code == 400
    assert "связанную привычку" in str(response.data).lower() or "вознаграждение" in str(response.data).lower()

@pytest.mark.django_db
def test_validation_fails_if_pleasant_habit_has_reward(auth_client):
    """Ошибка: приятная привычка не может иметь награду"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "10:00",
        "action": "чай",
        "execution_time": 60,
        "periodicity": 1,
        "is_pleasant": True,
        "reward": "печенье"
    }, format='json')

    assert response.status_code == 400
    assert "приятная привычка" in str(response.data).lower()

@pytest.mark.django_db
def test_validation_fails_if_pleasant_habit_has_related(auth_client, pleasant_habit):
    """Ошибка: приятная привычка не может иметь связанную"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "10:00",
        "action": "игра",
        "execution_time": 60,
        "periodicity": 1,
        "is_pleasant": True,
        "related_habit": pleasant_habit.id
    }, format='json')

    assert response.status_code == 400
    assert "приятная привычка" in str(response.data).lower()

# ----------------------------
# 📋 СПИСКИ ПРИВЫЧЕК
# ----------------------------

@pytest.mark.django_db
def test_get_only_user_habits(auth_client, user):
    """Пользователь видит только свои привычки"""
    Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="пресс",
        execution_time=60,
        periodicity=1
    )

    response = auth_client.get('/api/habits/')
    assert response.status_code == 200
    assert response.data["count"] == 1

@pytest.mark.django_db
def test_public_habits_list_visible(auth_client, user):
    """Публичные привычки видны через ?public=true"""
    Habit.objects.create(
        user=user,
        place="улица",
        time="07:00",
        action="бег",
        execution_time=100,
        periodicity=1,
        is_public=True
    )
    response = auth_client.get('/api/habits/?public=true')
    assert response.status_code == 200
    assert len(response.data["results"]) == 1

# ----------------------------
# 📲 MOCK: ОТПРАВКА TELEGRAM
# ----------------------------
@pytest.mark.django_db
@patch("habits.views.send_telegram_message.delay")
def test_telegram_notification_sent(mock_send, auth_client):
    """Уведомление отправляется в Telegram при создании привычки"""
    response = auth_client.post('/api/habits/', {
        "place": "дом",
        "time": "08:00",
        "action": "медитация",
        "execution_time": 60,
        "periodicity": 1
    }, format='json')

    assert response.status_code == 201
    mock_send.assert_called_once()
