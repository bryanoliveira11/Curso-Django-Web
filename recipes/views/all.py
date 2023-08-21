from os import environ

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from dotenv import load_dotenv

from recipes.models import Recipe
from utils.pagination import make_pagination

load_dotenv()

PER_PAGE = int(environ.get('PER_PAGE', 9))


def recipe(request, recipe_pk: int):
    recipe = get_object_or_404(
        Recipe.objects.filter(pk=recipe_pk, is_published=True))

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
        'title': f'{recipe} |'
    })
