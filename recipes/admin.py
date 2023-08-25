from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = '-pk',


class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'author', 'created_at', 'slug', 'is_published',
    list_editable = 'is_published',
    list_display_links = 'title', 'created_at',
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html',
    search_fields = 'id', 'title', 'description', 'preparation_steps',
    ordering = '-pk',
    list_per_page = 10
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [TagInline,]
