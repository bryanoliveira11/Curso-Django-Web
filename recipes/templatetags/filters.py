from django.template import Library

from utils import django_filters

register = Library()


@register.filter
def description_text(description):
    return django_filters.description_text(description)


@register.filter
def description_text_home(description):
    return django_filters.description_text_home(description)
