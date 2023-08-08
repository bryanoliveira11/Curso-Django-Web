import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def get_login_form(self):
        return self.browser.find_element(By.CLASS_NAME, 'main-form')

    def login_form_fill(self, username, password):
        # user opens the login pages
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_login_form()
        username_field = self.get_by_placeholder(form, 'Type Your Username')
        password_field = self.get_by_placeholder(form, 'Type Your Password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        form.submit()

    def test_empty_fields_error_message(self):
        # user types blank spaces in the form
        self.login_form_fill(username='  ', password='  ')

        self.assertIn(
            'Invalid Username or Password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_invalid_credentials_error_message(self):
        # user types invalid credentials
        self.login_form_fill(username='invalid_user', password='invalid_pass')

        # user sees error message
        self.assertIn(
            'Invalid Credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_valid_data_can_login_successfully(self):
        string_password = "Abc123"
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # user types correct login data
        self.login_form_fill(username=user.username, password=string_password)

        # successfull login
        self.assertIn(
            f'You are Logged in as {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
