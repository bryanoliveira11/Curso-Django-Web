from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from tag.models import Tag
from utils.strings import generate_random_string


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class RecipeManager(models.Manager):
    def get_published(self):
        ''' returns only published recipes '''
        return self.filter(is_published=True)


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(
        max_length=65, choices=(
            ('Minutes', 'Minutes'),
            ('Hours', 'Hours'),
        )
    )
    servings = models.IntegerField()
    servings_unit = models.CharField(
        max_length=65, choices=(
            ('Cups', 'Cups'),
            ('Slices', 'Slices'),
            ('Pieces', 'Pieces'),
        )
    )
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/cover/%Y/%m/%d/', blank=True, default=''
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}{generate_random_string(length=5)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):  # will add a button to admin page
        return reverse("recipes:recipe", args=(self.pk,))
