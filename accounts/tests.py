import re
from typing import List, Optional

from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile


class AccountsTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.create_url = reverse('user-create')

    def test_create_user_return_valid_token(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'short',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        # data will be like: {'password': ['Ensure this field has at least 8 characters.']}
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'f' * 151,
            'email': 'foobar@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'foobar@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexist_username(self):
        data = {
            'username': 'test',
            'email': 'foobar@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexist_email(self):
        data = {
            'username': 'foobar',
            'email': 'test@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobar',
            'email': 'testexample.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'somepassword',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class JWTTest(APITestCase):

    def setUp(self):
        self.user_credential = {
            'username': 'test',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        self.test_user = User.objects.create_user(**self.user_credential)
        self.login_url = reverse('jwt-create')
        self.token_verify_url = reverse('jwt-verify')
        self.token_refresh_url = reverse('jwt-refresh')

    def test_user_login_flow(self):
        login_response = self.client.post(self.login_url, self.user_credential, format='json')
        token = login_response.data['token']
        verify_response = self.client.post(self.token_verify_url, {'token': token}, format='json')

        self.assertEqual(token, verify_response.data['token'])

    def test_user_refresh_token(self):
        token = self.client.post(self.login_url, self.user_credential, format='json').data['token']

        refresh_response = self.client.post(self.token_refresh_url, self.user_credential, format='json')

        self.assertNotEqual(token, refresh_response.data['token'])


class SignupTest(APITestCase):

    def setUp(self):
        self.user_credential = {
            'username': 'test',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        self.signup_url = reverse('user-create')

    def test_new_signup_account_not_activated(self):
        signup_response = self.client.post(self.signup_url, self.user_credential, format='json')

        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(User.objects.last().is_active)

    def test_email_confirmation_is_sent(self):
        self.client.post(self.signup_url, self.user_credential, format='json')

        user = User.objects.last()
        self.assertEqual(len(mail.outbox), 1)
        confirmation_email = mail.outbox[0]
        self.assertIn(user.username, confirmation_email.body)
        urls = SignupTest.find_links(confirmation_email.body)
        self.assertTrue(urls)

    def test_activate_account(self):
        self.client.post(self.signup_url, self.user_credential, format='json')

        confirmation_email = mail.outbox[0]
        urls = SignupTest.find_links(confirmation_email.body)
        for url in urls:
            resp = self.client.get(url, follow=True)
            self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.last()
        self.assertEqual(user.is_active, True)

    @staticmethod
    def find_links(text: str) -> List[Optional[str]]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return urls


class TestProfile(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.test_user.is_active = True
        self.test_user.save()
        self.profile_url = reverse('profile')
        self.default_profile = {
            'age_range': '',
            'city': '',
            'state_province': '',
            'job_role': '',
            'job_category': '',
            'job_level': '',
            'job_years': 0,
            'education_degree': '',
            'education_school': '',
            'education_major': '',
            'education_year_graduated': 0,
            'interests': ''
        }

    def test_creating_user_model_also_creates_profile_model(self):
        user = User.objects.create()

        profile = user.profile
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, user)

    def test_saving_user_also_saves_profile(self):
        city_name_to_save = 'SF'
        user = User.objects.create()
        self.assertEqual(user.profile.city, '')

        user.profile.city = city_name_to_save
        user.save()

        new_profile = Profile.objects.get(user=user)
        self.assertEqual(new_profile.city, city_name_to_save)

    def test_get_user_profile(self):
        self.client.login(username='test', password='testpassword')
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self.default_profile)

    def test_cannot_access_profile_when_logout(self):
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        data = {
            'city': 'SF',
        }
        self.client.login(username='test', password='testpassword')
        resp = self.client.put(self.profile_url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {**self.default_profile, **data})

    def test_update_profile_with_wrong_data(self):
        data = {
            'permission': 'highest'
        }
        self.client.login(username='test', password='testpassword')
        resp = self.client.put(self.profile_url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self.default_profile)
