from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .serializers import UserSerializer


class LogoutViewTests(TestCase):
    def test_auth_token_gets_reset_on_logout(self):
        '''Logout should reset the auth token.'''
        client = APIClient()
        user = User.objects.create_user(
            username='test', email='test@test.com', password='test123')
        url = reverse('users:login')
        data = {
            'username': 'test',
            'password': 'test123'}
        # Login and get the first key
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)
        key = response.data['key']
        # Logout
        client.force_authenticate(user=user)
        response = client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Login again
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)
        self.assertNotEqual(response.data['key'], key)


class LoginViewTests(TestCase):
    def test_login_works_with_username(self):
        '''
        Login should return a token key
        if given good username/password.
        '''
        User.objects.create_user(
            username='test', email='test@test.com', password='test123')
        url = reverse('users:login')
        data = {
            'username': 'test',
            'password': 'test123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)

    def test_cant_login_with_bad_creds(self):
        '''
        Login should not return a token key
        if given bad password.
        '''
        User.objects.create_user(
            username='test', email='test@test.com', password='test123')
        url = reverse('users:login')
        data = {
            'username': 'test',
            'password': 'wrongpwd'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('key' not in response.data)


class RegisterUserTests(TestCase):
    def test_register_user(self):
        '''The reigster endpoint should create a new user.'''
        url = reverse('users:register')
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'testtest123',
            'password2': 'testtest123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')


class CurrentUserViewTests(TestCase):
    def test_anon_cannot_access(self):
        '''Anon user cannot access this endpoint.'''
        url = reverse('users:user_details')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access(self):
        '''Authenticated users can retrieve from here.'''
        user = User.objects.create_user(username='steve', email='s@s.com')
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users:user_details')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'erik', 'hall.erik@gmail.com', '1234')

    def test_gravatar_url(self):
        expected = 'http://www.gravatar.com/avatar/' \
                   '6764f0006df33b933b826c736d2e4274'
        self.assertEqual(self.user.profile.gravatar_url(), expected)
