from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path(
        'recipes/search/', views.RecipeListViewSearch.as_view(), name='search'
    ),
    path(
        'recipes/tags/<slug:slug>',
        views.RecipeListViewTag.as_view(), name='tags'
    ),
    path(
        'recipes/category/<int:category_pk>/',
        views.RecipeListViewCategory.as_view(), name='category'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetailView.as_view(), name='recipe'
    ),
    path('recipes/api/v1/', views.RecipeListViewHomeApi.as_view(),
         name='api_v1'
         ),
    path('recipes/api/v1/<int:pk>/', views.RecipeDetailViewApi.as_view(),
         name='api_v1_detail'
         ),
    path(
        'recipes/api/v2/',
        views.RecipeApiV2ViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='api_v2'
    ),
    path(
        'recipes/api/v2/<int:pk>/',
        views.RecipeApiV2ViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='api_v2_detail'
    ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.TagApiV2Detail.as_view(), name='api_v2_tag'
    ),
    path('recipes/theory/', views.theory, name='theory'),
]
