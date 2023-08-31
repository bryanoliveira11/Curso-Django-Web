from collections import defaultdict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from authors.validators import AuthorRecipeValidator
from tag.models import Tag

from .models import Recipe

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit',
            'preparation_steps', 'cover'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)

    preparation = serializers.SerializerMethodField(read_only=True)
    # field that references a method

    category = serializers.StringRelatedField(read_only=True)

    # uses the TagSerializer to get all the tag info
    tag_objects = TagSerializer(
        many=True, source='tags', read_only=True
    )

    # hyperlink for tags
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs, ErrorClass=serializers.ValidationError
        )
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)
