from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/category/<int:category_pk>/',
         views.category, name='category'),
    path('recipes/<int:recipe_pk>/', views.recipe, name='recipe'),
]
