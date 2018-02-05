import re
from typing import List, Optional

from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.create_url = reverse('account_create')

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
            'username': 'foo' * 30,
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
        self.login_url = reverse('login')
        self.token_verify_url = reverse('token-verify')
        self.token_refresh_url = reverse('token-refresh')

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
        self.signup_url = reverse('account_create')

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
            self.client.get(url)

        user = User.objects.last()
        self.assertEqual(user.is_active, True)

    @staticmethod
    def find_links(text: str) -> List[Optional[str]]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return urls
