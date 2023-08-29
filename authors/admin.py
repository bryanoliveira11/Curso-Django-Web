from django.contrib import admin

from authors.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'author_id', 'author', 'bio',
    list_display_links = 'author',
    search_fields = 'author',
