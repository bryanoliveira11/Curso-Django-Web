from django.contrib.auth import get_user_model
from rest_framework import serializers

from tag.models import Tag

from .models import Category, Recipe

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description',
            'author', 'category', 'tags',
            'public', 'preparation',
            'tag_objects', 'tag_links',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)

    preparation = serializers.SerializerMethodField(read_only=True)
    # field that references a method

    category = serializers.StringRelatedField(read_only=True)

    # uses the TagSerializer to get all the tag info
    tag_objects = TagSerializer(
        many=True, source='tags'
    )

    # hyperlink for tags
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        queryset=Tag.objects.all(),
        view_name='recipes:api_v2_tag'
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
