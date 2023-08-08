import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 5)

    def get_form(self):
        return self.browser.find_element(
            By.CLASS_NAME, 'main-form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + reverse('authors:register'))
        form = self.get_form()

        self.fill_form_data(form)
        form.find_element(By.NAME, 'email').send_keys('testmail@gmail')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'EX.: John')
            first_name_field.send_keys('  ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write Your First Name', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'EX.: Doe')
            last_name_field.send_keys('  ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write Your Last Name', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(
                form, 'Type Your Username')
            username_field.send_keys('  ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Your Username must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(
                form, 'Type Your Email')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Enter a valid email address.', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_not_matching(self):
        def callback(form):
            password1 = self.get_by_placeholder(
                form, 'Type Your Password')
            password2 = self.get_by_placeholder(
                form, 'Type Your Password')

            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Passwords Must Be Equal', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_success(self):
        self.browser.get(self.live_server_url + reverse('authors:register'))
        form = self.get_form()

        # typing valid information in all fields
        self.get_by_placeholder(form, 'EX.: John').send_keys('my first name')
        self.get_by_placeholder(form, 'EX.: Doe').send_keys('last name')
        self.get_by_placeholder(
            form, 'Type Your Username').send_keys('iamatestuser')
        self.get_by_placeholder(
            form, 'Type Your Email').send_keys('myemail@email.com')
        self.get_by_placeholder(
            form, 'Type Your Password').send_keys('Abc123456')
        self.get_by_placeholder(
            form, 'Repeat Your Password').send_keys('Abc123456')

        form.submit()

        self.assertIn(
            'User Created Succesfully. Please Log In.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
