"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('public', views.MentorPublicViewSet, 'mentor-public')
router.register('', views.MentorMemberOnlyViewSet, 'mentor-member-only')

urlpatterns = [
    path('', include(router.urls))
]
