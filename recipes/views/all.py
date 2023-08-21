from django.shortcuts import get_object_or_404, render

from recipes.models import Recipe


def recipe(request, recipe_pk: int):
    recipe = get_object_or_404(
        Recipe.objects.filter(pk=recipe_pk, is_published=True))

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
        'title': f'{recipe} |'
    })
