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

    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')
    email = forms.EmailField(required=True, label='E-mail')

    password = forms.CharField(
        required=True,
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
        required=True, widget=forms.PasswordInput(), label='Password 2'
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
        error_messages = {
            'username': {
                'required': 'This field must be not empty',
                'invalid': 'This field is invalid'
            }
        }
        widgets = {
            'password': forms.PasswordInput({
                'placeholder': 'Type Your Password'
            },
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords Must Be Equal',
                'password2': 'Passwords Must Be Equal'
            }, code='invalid'
            )

        email = cleaned_data.get('email')
        email_database = User.objects.filter(email=email).first()

        if email_database:
            raise ValidationError({
                'email': 'That Email is Already in Use.'
            })
