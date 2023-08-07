from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No Recipes Found', response.content.decode('utf-8'))

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_loads_recipes(self):
        # need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # self.assertIn('recipe title', content)
        # self.assertIn('14 minutos', content)
        # self.assertIn('3 pessoas', content)
        reponse_context_recipes = response.context['recipes']
        self.assertEqual(len(reponse_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        ''' Test if is_published False recipes are not showing  '''

        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No Recipes Found', response.content.decode('utf-8'))

    def test_recipe_home_is_paginated(self):
        self.make_multiple_recipes(number_of_recipes=2)

        with patch('recipes.views.PER_PAGE', new=1):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 1)
        self.assertEqual(len(paginator.get_page(2)), 1)

    def test_invalid_page_query_uses_page_one(self):
        self.make_multiple_recipes(number_of_recipes=2)

        with patch('recipes.views.PER_PAGE', new=1):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(
                1,
                response.context['recipes'].number)
