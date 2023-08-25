from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from utils.strings import generate_random_string


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # generic relation fields
    # represents the model that we will reference
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # represents the id of the model above
    object_id = models.CharField(max_length=255)
    # a field that represents the generic relationship of the above fields
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}{generate_random_string(length=5)}'
            self.slug = slug

        return super().save(*args, **kwargs)
