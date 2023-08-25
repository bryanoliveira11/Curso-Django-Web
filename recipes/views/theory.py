# from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Value
from django.db.models.aggregates import Count
from django.db.models.functions import Concat
from django.shortcuts import render

from recipes.models import Recipe


def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.all()
    # recipes = recipes.filter(title__icontains='Created').order_by('-id').last()
    # recipes = Recipe.objects.get(id=1)

    # try:
    #     recipes = Recipe.objects.get(id=1000)
    # except ObjectDoesNotExist:
    #     recipes = None

    # recipes = Recipe.objects.filter(
    #     Q(
    #         Q(title__icontains='a', id__gt=2) |
    #         Q(id__gt=1000)
    #     ),
    # )[:10]

    # F An object capable of resolving references to existing query objects.
    # recipes = Recipe.objects.filter(
    #     id=F('author__id')).order_by('-id', 'title')

    # .values returns a dict
    # recipes = Recipe.objects.values('id', 'title', 'author__username')[:10]

    # .only returns all fields that you select
    # recipes = Recipe.objects.only('id', 'title', 'is_published')

    # .defer returns all fields except the ones you select
    # recipes = Recipe.objects.defer('is_published')

    # Count
    # recipes = Recipe.objects.values('id', 'title').filter(
    #     title__icontains='rib'
    # )

    # annotate, F and Value classes
    # recipes = Recipe.objects.all().annotate(
    #     author_full_name=Concat(
    #         F('author__first_name'), Value(' '),
    #         F('author__last_name'), Value(' ('),
    #         F('author__username'), Value(')'),)
    # ).select_related('author')

    # using a manager method from the models.py
    recipes = Recipe.objects.get_published().select_related('author')

    # using Count
    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
    }

    return render(
        request, 'recipes/pages/theory.html', context=context)
