from django.urls import path
from habits import views

urlpatterns = [
    path('', views.HabitList.as_view(), name='habit-list'),
    path('<int:pk>/', views.HabitDetail.as_view(), name='habit-detail'),
    path('public/', views.PublicHabitList.as_view(), name='public-habit-list'),
]