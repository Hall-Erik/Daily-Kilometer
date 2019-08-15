from django.test import TestCase
from django.contrib.auth.models import User


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'erik', 'hall.erik@gmail.com', '1234')

    def test_gravatar_url(self):
        expected = 'http://www.gravatar.com/avatar/' \
                   '6764f0006df33b933b826c736d2e4274'
        self.assertEqual(self.user.profile.gravatar_url(), expected)
