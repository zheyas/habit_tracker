from django.urls import path
from habits.views import HabitListCreateView, HabitDetailView

urlpatterns = [
    path('', HabitListCreateView.as_view(), name='habit-list-create'),
    path('<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
]