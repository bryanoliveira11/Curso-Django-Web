# from django.test import TestCase
from unittest import TestCase

from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type Your Username'),
        ('email', 'Type Your Email'),
        ('first_name', 'EX.: John'),
        ('last_name', 'EX.: Doe'),
        ('password', 'Type Your Password'),
        ('password2', 'Repeat Your Password'),
    ])
    def test_fields_placeholders(self, field, placeholder):
        form = RegisterForm()
        field_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, field_placeholder)

    @parameterized.expand([
        'username', 'first_name', 'last_name', 'email', 'password', 'password2'
    ])
    def test_fields_required(self, field):
        form = RegisterForm()
        field_required = form[field].field.required

        self.assertEqual(True, field_required)

    @parameterized.expand([
        ('password', ('Password must have at least one uppercase letter, '
                      'one lowercase letter and one number. The length should be '
                      'at least 8 characteres.')),
        ('username', ('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        field_help_text = form[field].field.help_text

        self.assertEqual(help_text, field_help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('password', 'Password'),
        ('password2', 'Password 2'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        field_label = form[field].field.label

        self.assertEqual(label, field_label)
