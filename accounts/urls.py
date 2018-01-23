from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='account-create'),
    path('login/', obtain_jwt_token, name='login'),
    path('token-verify/', verify_jwt_token, name='token-verify'),
    path('token-refresh/', refresh_jwt_token, name='token-refresh'),
]
