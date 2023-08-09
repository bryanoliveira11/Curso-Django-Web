from django.utils.text import Truncator


def description_text(description):
    return Truncator(description).chars(62)


def description_text_home(description):
    return Truncator(description).chars(124)
