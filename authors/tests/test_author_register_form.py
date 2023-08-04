from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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
        ('username', ('Username must have letters, numbers or one of those @.+-_'
                      'The length must be between 4 and 150 characteres.')),
        ('email', ('The Email Must be Valid.'))
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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@gmail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Your Username must not be empty'),
        ('first_name', 'Write Your First Name'),
        ('last_name', 'Write Your Last Name'),
        ('email', 'Write Your Email'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(
            'Username must have at least 4 characteres',
            response.context['form'].errors.get('username')
        )

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(
            'Username must have less than 150 characteres',
            response.context['form'].errors.get('username')
        )

    def test_password_field_is_strong(self):
        # test with invalid password
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password must have at least one uppercase letter, ' \
            'one lowercase letter and one number. The length should ' \
            'be at least 8 characteres.'

        self.assertIn(msg, response.context['form'].errors.get('password'))

        # test with valid password
        self.form_data['password'] = 'abc123456A'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        # different passwords will generate error
        self.form_data['password'] = 'abc123456A'
        self.form_data['password2'] = 'A123456abc'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(
            'Passwords Must Be Equal',
            response.context['form'].errors.get('password')
        )
        self.assertIn(
            'Passwords Must Be Equal',
            response.context['form'].errors.get('password2')
        )

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.post(url)
        self.assertEqual(404, response.status_code)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This Email is Already in Use.'

        self.assertIn(msg, response.context['form'].errors.get('email'))

        self.assertIn(msg, response.content.decode('utf-8'))
