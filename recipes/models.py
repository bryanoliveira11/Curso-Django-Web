import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

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
        return self.filter(is_published=True).order_by('-id')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
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
    tags = models.ManyToManyField(Tag, blank=True, default='')

    # resize image function
    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize(
            (new_width, new_height), Image.LANCZOS
        )

        new_image.save(image_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}{generate_random_string(length=5)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, new_width=840)
            except FileNotFoundError:
                ...

        return saved

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):  # will add a button to admin page
        return reverse("recipes:recipe", args=(self.pk,))

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_database = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_database:
            if recipe_database.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
