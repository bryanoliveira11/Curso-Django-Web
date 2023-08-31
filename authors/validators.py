from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.length_msg = 'Must Have at Least 5 Characteres.'
        self.clean()

    def validate_field_length(self, field_name: str, field_value: str, min_length: int):
        if field_value:
            if len(field_value) < min_length:
                error_message = f'Must Have at Least {min_length} Characteres.'
                self.errors[field_name].append(error_message)

    def clean(self, *args, **kwargs):
        cleaned_data = self.data
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
            self.errors['title'].append(
                'Cannot be Equal to Description.'
            )
            self.errors['description'].append(
                'Cannot be Equal to Title.'
            )

        if not is_positive_number(prep_time):  # prep time int is valid
            self.errors['preparation_time'].append(
                'Must be a Positive Number.'
            )

        if not is_positive_number(servings):  # servings int is valid
            self.errors['servings'].append(
                'Must be a Positive Number.'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)
