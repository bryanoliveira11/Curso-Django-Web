from time import sleep
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)  # http://127.0.0.1:8000/
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No Recipes Found Here', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_multiple_recipes(number_of_recipes=2)

        title_expected = "This is the First Recipe"
        recipes[0].title = title_expected
        recipes[0].save()

        # User opens the page
        self.browser.get(self.live_server_url)

        # Sees a search field
        search_field = self.browser.find_element(By.CLASS_NAME, 'search-input')

        # User Clicks at the field and type something to search
        search_field.send_keys(title_expected)
        search_field.send_keys(Keys.ENTER)

        self.assertIn(
            title_expected,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=1)  # 1 recipe per page
    def test_recipe_home_page_pagination(self):
        self.make_multiple_recipes(number_of_recipes=2)  # two recipes created

        # User opens the page
        self.browser.get(self.live_server_url)

        # User sees the pagination and clicks on the page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # User sees one more recipe on the page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 1
        )
