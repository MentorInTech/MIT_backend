from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import User
from programs.models import Program
from django.urls import reverse
from rest_framework import status


class TestModel(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.test_profile = user.profile

    def test_empty_goals(self):
        self.assertEqual(len(self.test_profile.program_set.all()), 0)

    def test_assign_new_goal(self):
        program = Program.objects.create(title='A Program', role='MTR', score=10, profile=self.test_profile)
        self.assertEqual(len(self.test_profile.program_set.all()), 1)
        self.assertEqual(self.test_profile.program_set.all()[0], program)


class TestAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.client.login(username='test', password='testpassword')
        self.programs_url = reverse('program_list')

    def test_list_empty_goals(self):
        resp = self.client.get(self.programs_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_create_goal(self):
        data = {
            'title': 'random',
            'role': 'MTR',
            'score': 8,
        }
        resp = self.client.post(self.programs_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        programs = self.client.get(self.programs_url).data
        self.assertTrue(all(
            item in programs[-1].items() for item in data.items()
        ))

    def test_get_detail(self):
        program = Program.objects.create(title='A Program', role='MTR', score=10, profile=self.user.profile)

        program_resp = self.client.get(f'{self.programs_url}{program.id}/')

        self.assertEqual(program_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(program_resp.data['title'], program.title)
        self.assertEqual(program_resp.data['role'], program.role)
        self.assertEqual(program_resp.data['score'], program.score)
