from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_pk>/',
         views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:recipe_pk>/', views.recipe, name='recipe'),
]
