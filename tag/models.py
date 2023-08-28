from django.db import models
from django.utils.text import slugify

from utils.strings import generate_random_string


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}{generate_random_string(length=5)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
