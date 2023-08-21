from os import environ
from typing import Any, Dict

from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.views.generic import ListView
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

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


class RecipeListViewCategory(RecipeListViewBase):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_pk'), is_published=True
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        print(ctx)
        ctx.update({
            'title': f'{ctx.get("object_list")[0].category} '  # type:ignore
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

        qs = qs.filter(
            Q(
                Q(title__icontains=self.search_term) |
                Q(description__icontains=self.search_term)
            ),
            is_published=True
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            'title': f'Search for "{self.search_term}"',
            'search_term': self.search_term,
            'additional_url_query': f'&q={self.search_term}'
        })

        return ctx
