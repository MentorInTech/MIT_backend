from django.test import TestCase
from accounts.models import User
from goals.models import Goal


class TestModel(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.test_profile = user.profile

    def test_empty_goals(self):
        self.assertEqual(len(self.test_profile.goals.all()), 0)

    def test_assign_new_goal(self):
        goal = Goal.objects.create(program_title='A Program', role='MTR', score=10)
        self.test_profile.goals.add(goal)
        self.assertEqual(len(self.test_profile.goals.all()), 1)
        self.assertEqual(self.test_profile.goals.all()[0], goal)
