from django import forms
from django.core.exceptions import ValidationError

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    cover = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'span-2'
            }
        ),
    )
    servings_unit = forms.CharField(
        widget=forms.Select(
            choices=(
                ('Cups', 'Cups'),
                ('Slices', 'Slices'),
                ('Pieces', 'Pieces'),
            )
        )
    )
    preparation_time_unit = forms.CharField(
        widget=forms.Select(
            choices=(
                ('Minutes', 'Minutes'),
                ('Hours', 'Hours'),
            )
        )
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description',
            'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit',
            'preparation_steps', 'cover'
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
