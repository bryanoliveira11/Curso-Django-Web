from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'authors'

authors_api_v2_router = SimpleRouter()
authors_api_v2_router.register(
    'api', views.AuthorsApiV2ViewSet, basename='authors-api'
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/recipe/new/',
         views.DashboardRecipe.as_view(),
         name='dashboard_recipe_new'
         ),
    path('dashboard/recipe/<int:id>/edit/',
         views.DashboardRecipe.as_view(),
         name='dashboard_recipe_edit'
         ),
    path('dashboard/recipe/<int:id>/delete/',
         views.DashboardRecipeDelete.as_view(),
         name='dashboard_recipe_delete'
         ),
    path('profile/<int:id>/',
         views.ProfileView.as_view(),
         name='profile'
         ),
    path('', include(authors_api_v2_router.urls))
]
