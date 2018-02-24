"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
]
