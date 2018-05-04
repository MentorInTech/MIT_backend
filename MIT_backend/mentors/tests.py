"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""

from django.urls import reverse
from django.test.client import Client
from rest_framework import status
import pytest
from django.contrib.auth.models import User

from .models import Mentor
from ..accounts.factories import UserFactory


@pytest.fixture
def mentor(db):
    _mentor = UserFactory()
    Mentor.objects.create(profile=_mentor.profile)
    return _mentor


@pytest.fixture
def user(db):
    return UserFactory()


PRIVATE_PROFILE_FIELDS = ('education_degree', 'education_school',
                          'education_major', 'education_year_graduated',)


def test_get_mentors_public(client: Client, mentor: User):

    resp = client.get(reverse('mentor-public-list'))
    assert resp.status_code == status.HTTP_200_OK

    mentor_data = resp.data[0]['profile']
    assert mentor_data['user']['username'] == mentor.username

    for field in PRIVATE_PROFILE_FIELDS:
        assert field not in mentor_data


def test_get_mentors_private(client: Client, mentor: User, user: User):
    assert client.login(username=user.username, password='password123')
    resp = client.get(reverse('mentor-member-only-list'))
    assert resp.status_code == status.HTTP_200_OK

    mentor_data = resp.data[0]['profile']
    assert mentor_data['user']['username'] == mentor.username

    for field in PRIVATE_PROFILE_FIELDS:
        assert field in mentor_data
