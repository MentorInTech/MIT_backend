from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AccountsTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'testpassword')
        self.create_url = reverse('account-create')

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
