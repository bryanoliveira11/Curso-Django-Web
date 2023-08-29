from os import environ
from typing import Any, Dict

from django.db.models import Q
from django.http import Http404
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from dotenv import load_dotenv

from recipes.models import Recipe
from tag.models import Tag
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
        html_language = translation.get_language()

        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': 'Home',
            'html_language': html_language,
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')

        return qs


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


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
        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} '  # type:ignore
            f'- {category_translation}'
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


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def __init__(self, *args, **kwargs) -> None:
        self.search_term = None
        super().__init__(**kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag'

        ctx.update({
            'title': page_title,
        })

        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True,
        })

        return ctx
