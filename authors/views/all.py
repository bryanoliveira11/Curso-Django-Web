from os import environ
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PER_PAGE_DASHBOARD', 3))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'title': 'Register',
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)  # password encrypt
        user.save()
        messages.success(request, 'User Created Succesfully. Please Log In.')

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login.html', {
        'title': 'Login',
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'You Are Logged In.')
            login(request, user=authenticated_user)
        else:
            messages.error(request, 'Invalid Credentials')
    else:
        messages.error(request, 'Invalid Username or Password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid Logout Request.')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid Logout User.')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged Out Succesfully.')
    logout(request)
    return redirect(reverse('authors:login'))


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class Dashboard(ListView):
    model = Recipe
    context_object_name = 'user_recipes'
    template_name = 'authors/pages/dashboard.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('user_recipes'), PER_PAGE
        )

        ctx.update({
            'recipes': page_obj,
            'title': 'Dashboard',
            'pagination_range': pagination_range
        })

        return ctx

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(author=self.request.user, is_published=False)
        qs = qs.select_related('author', 'category')

        return qs
