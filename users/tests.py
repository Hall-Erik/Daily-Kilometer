from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .forms import UserRegisterForm


class RegisterViewTests(TestCase):
    def test_fields_appear(self):
        '''
        Anon user can visit view.
        '''
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password')

    def test_post_valid_data(self):
        response = self.client.post(
            reverse('users:register'), {
                'username': 'test',
                'email': 'test@test.com',
                'password1': 'python123',
                'password2': 'python123',
            }, follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertContains(
            response, 'Your account has been created. Please log in.')

    def test_post_invalid_data(self):
        response = self.client.post(
            reverse('users:register'), {
                'username': '',
                'email': '',
                'password1': 'python1111',
                'password2': 'python123',
            }, follow=True)
        self.assertNotContains(
            response, 'Your account has been created. Please log in.')

    def test_logged_in_user(self):
        '''
        Authenticated user is redirected.
        '''
        User.objects.create_user('test', None, '1234')
        self.client.login(username='test', password='1234')
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 302)


class PofileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test', None, '1234')

    def test_anon_user_redirect(self):
        '''
        Anonymous user can visit a profile.
        '''
        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_registered_users_can_visit_other_profiles(self):
        '''
        Registered users can visit other users' profiles.
        '''
        User.objects.create_user('steve', None, '1234')
        self.client.login(username='steve', password='1234')
        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_registered_user_can_visit_own_profile(self):
        '''
        Registered users can visit their profile.
        '''
        self.client.login(username='test', password='1234')
        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)


class RegisterFormTests(TestCase):
    def test_register_form_valid(self):
        form = UserRegisterForm(data={
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'python123',
            'password2': 'python123',
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form = UserRegisterForm(data={
            'username': '',
            'email': '123',
            'password1': 'python11111',
            'password2': 'python123',
        })
        self.assertFalse(form.is_valid())


class ProileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'erik', 'hall.erik@gmail.com', '1234')

    def test_gravatar_url(self):
        expected = 'http://www.gravatar.com/avatar/' \
                   '6764f0006df33b933b826c736d2e4274'
        self.assertEqual(self.user.profile.gravatar_url(), expected)
