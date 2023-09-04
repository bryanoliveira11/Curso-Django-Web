from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeApiV2Test(test.APITestCase, RecipeMixin):
    def get_api_list(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        return response

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_api_list()
        self.assertEqual(response.status_code, 200)

    def test_recipe_api_detail_returns_status_code_200(self):
        self.make_recipe()
        api_url = reverse('recipes:recipes-api-detail', kwargs={'pk': 1})
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.rest_framework.RecipeApiV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        number_of_recipes = 7
        self.make_multiple_recipes(number_of_recipes=number_of_recipes)
        response = self.client.get(reverse('recipes:recipes-api-list'))
        qtd_of_loaded_recipes = len(
            response.data.get('results')  # type:ignore
        )
        self.assertEqual(
            qtd_of_loaded_recipes, number_of_recipes
        )

    def test_recipe_api_list_do_not_show_unpublished_recipes(self):
        recipes = self.make_multiple_recipes(number_of_recipes=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()

        response = self.get_api_list()
        self.assertEqual(len(response.data.get('results')), 1)  # type:ignore
