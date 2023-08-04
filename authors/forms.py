import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', f'{placeholder_val}'.strip())


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characteres.',
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type Your Username')
        add_placeholder(self.fields['email'], 'Type Your Email')
        add_placeholder(self.fields['first_name'], 'EX.: John')
        add_placeholder(self.fields['last_name'], 'EX.: Doe')
        add_placeholder(self.fields['password'], 'Type Your Password')
        add_placeholder(self.fields['password2'], 'Repeat Your Password')

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'Your Username must not be empty',
            'min_length': 'Username must have at least 4 characteres',
            'max_length': 'Username must have less than 150 characteres'
        },
        help_text=(
            'Username must have letters, numbers or one of those @.+-_'
            'The length must be between 4 and 150 characteres.'
        ),
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        label='First Name',
        error_messages={'required': 'Write Your First Name'})

    last_name = forms.CharField(
        label='Last Name',
        error_messages={
            'required': 'Write Your Last Name'})

    email = forms.EmailField(
        label='E-mail',
        help_text='The Email Must be Valid.',
        error_messages={'required': 'Write Your Email'})

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characteres.'
        ),
        label='Password',
        validators=[strong_password]
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password 2',
        error_messages={'required': 'Please, repeat your password'}
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):  # validating if email already exists in database
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email=email).exists()

        if email_database:
            raise ValidationError(
                'This Email is Already in Use.', code='invalid'
            )

        return email

    def clean(self):  # validating passwords
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords Must Be Equal',
                'password2': 'Passwords Must Be Equal'
            }, code='invalid'
            )
