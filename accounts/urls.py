from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='account_create'),
    re_path(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.ActivateAccount.as_view(), name='activate_account'),
    path('login/', obtain_jwt_token, name='login'),
    path('token-verify/', verify_jwt_token, name='token-verify'),
    path('token-refresh/', refresh_jwt_token, name='token-refresh'),

    path('profile/', views.Profile.as_view(), name='profile'),
]
