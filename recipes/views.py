from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.all().order_by('-pk').filter(is_published=True)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': 'Home'
    })


def recipe(request, recipe_pk: int):
    recipe = get_object_or_404(
        Recipe.objects.filter(pk=recipe_pk, is_published=True))

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
        'title': f'{recipe} |'
    })


def category(request, category_pk: int):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_pk, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category'  # type:ignore
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-pk')

    if not recipes:
        search_term = ""

    return render(request, 'recipes/pages/search.html', context={
        'title': f'Search for "{search_term}"',
        'search_term': search_term,
        'recipes': recipes,
    })
