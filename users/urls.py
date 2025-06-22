from django.urls import path
from users import views
#from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserCreate.as_view(), name='user-create'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
    #path('token/', obtain_auth_token, name='api_token_auth')
]