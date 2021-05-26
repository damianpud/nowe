from django.test import TestCase
from django.urls import reverse

from .models import Profile, User


class ProfileTest(TestCase):

    def setUp(self):
        user = User(username='User', email='user@gmail.com')
        self.user = user
        user_password = 'password'
        self.user_password = user_password
        user.set_password(self.user_password)
        user.save()
        profile = Profile(biography='User biography', image='user.jpg')
        profile.user = user
        profile.save()

    def test_create_valid_user(self):
        data = {
            'username': 'User',
            'password': 'password',
            'email': 'user@email.com',
        }
        response = self.client.post(reverse('accounts:sign_up'), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_profile_exists(self):
        profile_count = Profile.objects.all().count()
        self.assertEqual(profile_count, 1)

    def test_user_password(self):
        self.assertTrue(self.user.check_password(self.user_password))
        self.assertFalse(self.user.check_password('incorrect_password'))

    def test_login_url(self):
        data = {
            'username': self.user.username,
            'password': self.user_password
        }
        response = self.client.post(reverse('accounts:login'), data, follow=True)
        redirect_path = response.request.get('PATH_INFO')
        self.assertEqual(redirect_path, reverse('index'))
        self.assertEqual(response.status_code, 200)

