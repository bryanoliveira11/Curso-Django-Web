from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', f'{placeholder_val}'.strip())


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your Username')
        add_placeholder(self.fields['email'], 'Your Email')
        add_placeholder(self.fields['first_name'], 'EX.: John')
        add_placeholder(self.fields['last_name'], 'EX.: Doe')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your Password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characteres.'
        )
    )

    password2 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat Your Password'
        })
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
        # labels = {
        #     'username': 'Username',
        # }

        # help_texts = {
        #     'email': 'The email must be valid.'
        # }
        error_messages = {
            'username': {
                'required': 'This field must be not empty',
                'invalid': 'This field is invalid'
            }
        }
        widgets = {
            'password': forms.PasswordInput({
                'placeholder': 'Type Your Password'
            }
            )
        }

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')

    #     if password != password2:
    #         raise ValidationError(
    #             'Passwords Must Be the Same', code='invalid'
    #         )

    #     return password

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
