from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', views.UserActivationView.as_view(), name='user-activate-get'),

    path('profile/', views.Profile.as_view(), name='profile'),
]
