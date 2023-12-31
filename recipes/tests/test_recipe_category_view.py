from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_pk': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        ''' Test if is_published False recipes are not showing  '''

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_pk': recipe.category.id}))  # type:ignore

        self.assertEqual(response.status_code, 404)
