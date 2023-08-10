from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    cover = forms.CharField(
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

    def validate_field_length(self, field_name: str, field_value: str, min_length: int):
        if len(field_value) < min_length:
            error_message = f'Must Have at Least 5 Characteres.'
            self._my_errors[field_name].append(error_message)

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        prep_time = cleaned_data.get('preparation_time')
        servings = cleaned_data.get('servings')
        prep_steps = cleaned_data.get('preparation_steps')

        self.validate_field_length(  # validate title length
            field_name='title', field_value=title, min_length=5
        )

        self.validate_field_length(  # description title length
            field_name='description', field_value=description, min_length=5
        )

        self.validate_field_length(  # prep_steps title length
            field_name='preparation_steps', field_value=prep_steps, min_length=5
        )

        if title == description:  # title = description
            self._my_errors['title'].append(
                'Cannot be Equal to Description.'
            )
            self._my_errors['description'].append(
                'Cannot be Equal to Title.'
            )

        if not is_positive_number(prep_time):  # prep time int is valid
            self._my_errors['preparation_time'].append(
                'Must be a Positive Number.'
            )

        if not is_positive_number(servings):  # servings int is valid
            self._my_errors['servings'].append(
                'Must be a Positive Number.'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
