from rest_framework import generics, permissions, pagination, status
from rest_framework.response import Response
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.tasks import send_telegram_message


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Список привычек текущего пользователя и создание новой.
    Параметр ?public=true — для просмотра публичных привычек.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        is_public = self.request.query_params.get('public')
        if is_public == 'true':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        # Отправляем сообщение в Telegram при создании привычки
        chat_id = getattr(habit.user, 'telegram_chat_id', None)
        if chat_id:
            message = f"Создана привычка: {habit.action} в {habit.place} в {habit.time}"
            send_telegram_message.delay(chat_id=chat_id, text=message)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление привычки пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
