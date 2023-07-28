import os
import string
import sys
from pathlib import Path
from random import choice
from secrets import SystemRandom

import django
from django.conf import settings
from django.utils.text import slugify

DJANGO_BASE_DIR = Path(__file__).parent.parent.parent
NUMBER_OF_OBJECTS = 100

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    from django.contrib.auth.models import User
    from faker import Faker
    from faker_food import FoodProvider

    from recipes.models import Category, Recipe

    Category.objects.all().delete()

    faker = Faker()
    faker.add_provider(FoodProvider)

    categories = ['Café da Manhã', 'Carnes', 'Vegano']  # categories
    django_categories = [Category(name=name) for name in categories]

    author = [faker.first_name() for _ in range(10)]  # random authors
    django_author = [User(username=name) for name in author]

    for category in django_categories:
        category.save()

    for author in django_author:
        author.save()

    # change images dir here.
    COVER_IMAGES_DIR = DJANGO_BASE_DIR / 'media' / 'images_used'

    covers = os.listdir(COVER_IMAGES_DIR)

    django_recipes = []

    for _ in range(NUMBER_OF_OBJECTS):
        title = faker.dish()
        description = faker.dish_description()
        slug = f'{slugify(title)}-{"".join(SystemRandom().choices(string.ascii_letters, k=5))}'
        prep_time = faker.random_number(digits=2, fix_len=True)
        prep_unit = 'Minutos'
        serv_time = faker.random_number(digits=2, fix_len=True)
        serv_unit = 'Porções'
        prep_steps = f'Ingredients : {[faker.ingredient() for _ in range(4)]}'
        cover = choice(covers)
        category = choice(django_categories)
        author = choice(django_author)

        django_recipes.append(
            Recipe(
                title=title,
                description=description,
                slug=slug,
                preparation_time=prep_time,
                preparation_time_unit=prep_unit,
                servings=serv_time,
                servings_unit=serv_unit,
                preparation_steps=prep_steps,
                preparation_steps_is_html=False,
                is_published=True,
                cover=cover,
                category=category,
                author=author
            )
        )

    if len(django_recipes) > 0:
        Recipe.objects.bulk_create(django_recipes)
