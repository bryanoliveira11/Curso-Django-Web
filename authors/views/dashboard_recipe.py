from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_recipe(self, id=None):  # get a recipe method
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                author=self.request.user, is_published=False, pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):  # render method
        return render(self.request, 'authors/pages/dashboard_recipe.html', context={
            'form': form,
            'title': f'Dashboard ({self.request.user})',
        })

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form=form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            # valid form to save
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()
            messages.success(request, 'Recipe Saved Successfully !')

            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(recipe.pk,))
            )

        return self.render_recipe(form=form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()  # type:ignore
        messages.success(self.request, 'Recipe Deleted Successfully.')
        return redirect(reverse('authors:dashboard'))
