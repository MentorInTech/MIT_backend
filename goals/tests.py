from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import User
from goals.models import Goal
from django.urls import reverse
from rest_framework import status


class TestModel(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.test_profile = user.profile

    def test_empty_goals(self):
        self.assertEqual(len(self.test_profile.goal_set.all()), 0)

    def test_assign_new_goal(self):
        goal = Goal.objects.create(program_title='A Program', role='MTR', score=10, profile=self.test_profile)
        self.assertEqual(len(self.test_profile.goal_set.all()), 1)
        self.assertEqual(self.test_profile.goal_set.all()[0], goal)


class TestAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.client.login(username='test', password='testpassword')
        self.goal_url = reverse('goal')

    def test_list_empty_goals(self):
        resp = self.client.get(self.goal_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_create_goal(self):
        data = {
            'program_title': 'random',
            'role': 'MTR',
            'score': 8,
        }
        resp = self.client.post(self.goal_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        goals = self.client.get(self.goal_url).data
        self.assertEqual([data], goals)
