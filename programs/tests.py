"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from programs.models import Program


class TestModel(TestCase):
    def setUp(self):
        self.mentor = User.objects.create_user('mentor', 'mentor@example.com', 'testpassword')
        self.mentee = User.objects.create_user('mentee', 'mentee@example.com', 'testpassword')

    def test_empty_program(self):
        self.assertEqual(len(self.mentor.mentor_programs.all()), 0)
        self.assertEqual(len(self.mentee.mentee_programs.all()), 0)

    def test_assign_new_program(self):
        program = Program.objects.create(title='A Program', mentor=self.mentor, mentee=self.mentee)
        self.assertEqual(len(self.mentor.mentor_programs.all()), 1)
        self.assertEqual(self.mentor.mentor_programs.all()[0], program)


class TestAPI(APITestCase):
    def setUp(self):
        self.mentor = User.objects.create_user('mentor', 'mentor@example.com', 'testpassword')
        self.mentee = User.objects.create_user('mentee', 'mentee@example.com', 'testpassword')
        self.client.login(username='mentee', password='testpassword')
        self.programs_url = reverse('program-list')

    def test_list_empty_goals(self):
        resp = self.client.get(self.programs_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_create_program(self):
        data = {
            'title': 'random',
            'mentor': self.mentor.id,
            'mentee': self.mentee.id,
        }
        resp = self.client.post(self.programs_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        programs = self.client.get(self.programs_url).data
        self.assertTrue(all(
            item in programs[-1].items() for item in data.items()
        ))

    def test_get_detail(self):
        program = Program.objects.create(title='A Program', score=10, mentor=self.mentor, mentee=self.mentee)

        program_resp = self.client.get(f'{self.programs_url}{program.id}/')

        self.assertEqual(program_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(program_resp.data['title'], program.title)
        self.assertEqual(program_resp.data['score'], program.score)
        self.assertEqual(program_resp.data['mentee'], program.mentee.id)
        self.assertEqual(program_resp.data['mentor'], program.mentor.id)

    def test_update_program(self):
        program = Program.objects.create(title='A Program', score=1, mentor=self.mentor, mentee=self.mentee)
        detail_url = reverse('program-detail', kwargs={'pk': program.id})
        old_program = self.client.get(detail_url).data
        new_program = {**old_program, 'score': 10}

        program_resp = self.client.put(detail_url, new_program)

        self.assertEqual(program_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(program_resp.data['score'], new_program['score'])
