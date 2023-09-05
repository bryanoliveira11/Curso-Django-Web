from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeApiV2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self):
        api_url = reverse('recipes:recipes-api-list')
        return api_url

    def get_api_list(self, additional_query=None):
        api_url = self.get_recipe_list_reverse_url()
        api_url = api_url if not additional_query else api_url + additional_query
        response = self.client.get(api_url)  # type:ignore
        return response

    def get_jwt_token_data(self, username='user', password='pass'):
        user_data = {
            'username': username,
            'password': password
        }
        user = self.make_author(**user_data)
        response = self.client.post(  # type:ignore
            reverse('recipes:token_obtain_pair'),
            data=user_data
        )

        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user
        }

    def get_recipe_raw_data(self):
        return {"title": "my title",
                "description": "my description",
                "preparation_time": 2,
                "preparation_time_unit": "Minutes",
                "servings": 3,
                "servings_unit": "Slices",
                "preparation_steps": "steps"}


class RecipeApiV2Test(test.APITestCase, RecipeApiV2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_api_list()
        self.assertEqual(response.status_code, 200)

    def test_recipe_api_detail_returns_status_code_200(self):
        recipe = self.make_recipe()
        api_url = reverse(
            'recipes:recipes-api-detail',
            kwargs={'pk': recipe.id}  # type:ignore
        )
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

    def test_recipe_api_list_loads_recipes_by_category(self):
        id_wanted = 5
        self.make_multiple_recipes(number_of_recipes=5)
        response = self.get_api_list(
            additional_query=f'?category_id={id_wanted}'
        )

        self.assertEqual(len(response.data.get('results')), 1)  # type:ignore
        self.assertEqual(
            response.data.get('results')[0].get('category'),  # type:ignore
            id_wanted
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)  # unauthorized

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        data = self.get_recipe_raw_data()
        access_token = self.get_jwt_token_data().get('jwt_access_token')  # type:ignore
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        self.assertEqual(
            response.status_code, 201  # created
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # configurations
        recipe = self.make_recipe()
        access_token = self.get_jwt_token_data(username='test_patch')
        author = access_token.get('user')
        recipe.author = author
        recipe.save()

        new_title = f'new title by {author.username}'  # type:ignore

        # actions
        response = self.client.patch(
            reverse(
                'recipes:recipes-api-detail', args=(recipe.id,)),  # type:ignore
            data={'title': new_title},
            HTTP_AUTHORIZATION=f'Bearer {access_token.get("jwt_access_token")}'
        )

        # assertions
        self.assertEqual(
            response.data.get('title'), new_title  # type:ignore
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_other_user(self):
        # configurations
        recipe = self.make_recipe()
        access_token = self.get_jwt_token_data(username='test_patch')

        # actual owner
        author = access_token.get('user')
        recipe.author = author
        recipe.save()

        # user that will try to update data
        another_user = self.get_jwt_token_data(username='cant_update')

        # actions
        response = self.client.patch(
            reverse(
                'recipes:recipes-api-detail', args=(recipe.id,)),  # type:ignore
            HTTP_AUTHORIZATION=f'Bearer {another_user.get("jwt_access_token")}'
        )

        # assertions
        self.assertEqual(
            response.status_code, 403  # forbidden
        )
