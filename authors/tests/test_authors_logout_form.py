from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username=user.username, password='my_pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid Logout Request.',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username=user.username, password='my_pass')

        # logged user is "my_user"
        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'another_user'},
            follow=True
        )

        self.assertIn(
            'Invalid Logout User.',
            response.content.decode('utf-8')
        )

    def test_user_logout_successfully(self):
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username=user.username, password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': user.username},
            follow=True
        )

        self.assertIn(
            'Logged Out Succesfully.',
            response.content.decode('utf-8')
        )
