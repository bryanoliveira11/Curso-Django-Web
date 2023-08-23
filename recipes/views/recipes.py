from os import environ
from typing import Any, Dict

from django import http
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView
from dotenv import load_dotenv

from recipes.models import Recipe
from utils.pagination import make_pagination

load_dotenv()

PER_PAGE = int(environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE
        )
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': 'Home',
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        return qs


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_dict = recipes.object_list.values()

        return JsonResponse(list(recipes_dict), safe=False)


class RecipeListViewCategory(RecipeListViewBase):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_pk'), is_published=True
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} '  # type:ignore
            '- Category'
        })
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def __init__(self, *args, **kwargs) -> None:
        self.search_term = None
        super().__init__(**kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        self.search_term = self.request.GET.get('q', '').strip()

        if not self.search_term:
            raise Http404()

        qs = qs.filter(
            Q(
                Q(title__icontains=self.search_term) |
                Q(description__icontains=self.search_term)
            ),
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'Search for "{self.search_term}"',
            'search_term': self.search_term,
            'additional_url_query': f'&q={self.search_term}'
        })

        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True,
        })

        return ctx


class RecipeDetailViewApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del (recipe_dict['is_published'])
        del (recipe_dict['preparation_steps_is_html'])

        return JsonResponse(recipe_dict, safe=False)
