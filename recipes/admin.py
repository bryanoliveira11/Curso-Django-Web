from django.contrib import admin

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = '-pk',


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'slug', 'is_published',
    list_editable = 'is_published',
    list_display_links = 'title',
    ordering = '-pk',
    list_per_page = 50
