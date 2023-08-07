from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By

# from django.test import LiveServerTestCase


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)  # http://127.0.0.1:8000/
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No Recipes Found Here', body.text)
