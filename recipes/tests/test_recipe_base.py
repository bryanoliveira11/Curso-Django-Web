from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name='User',
            last_name='name',
            username='username',
            password='123456',
            email='username@gmail.com'):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            title='recipe title',
            description='description',
            slug='recipe-slug',
            preparation_time=14,
            preparation_time_unit='Minutes',
            servings=3,
            servings_unit='Slices',
            preparation_steps='preparation',
            preparation_steps_is_html=False,
            is_published=True,
            cover=None,
            category_data=None,
            author_data=None,):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover,
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
        )

    def make_multiple_recipes(self, number_of_recipes=2):
        recipes = []

        for i in range(number_of_recipes):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
