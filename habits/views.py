from rest_framework import generics, permissions
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.tasks import send_telegram_message
from rest_framework.response import Response
from rest_framework import status

class HabitList(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        # Отправляем сообщение в Telegram при создании привычки
        if habit.user.telegram_chat_id:  # Предполагаем, что у User есть поле telegram_chat_id
            text = f"Создана привычка: {habit.action} в {habit.place} в {habit.time}"
            send_telegram_message.delay(chat_id=habit.user.telegram_chat_id, text=text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
             return Response(serializer.data, status=status.HTTP_201_CREATED)

class PublicHabitList(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.filter(is_public=True)

class HabitList(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class PublicHabitList(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.filter(is_public=True)


