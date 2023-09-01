from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeApiV2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]  # type:ignore
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1, category_id=2,
            tags=[1, 2]
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RecipeApiV2Detail(APIView):
    def get_recipe(self, pk):
        return get_object_or_404(
            Recipe.objects.get_published(), pk=pk  # type:ignore
        )

    def get(self, request, **kwargs):
        recipe = self.get_recipe(kwargs.get('pk'))

        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, **kwargs):
        recipe = self.get_recipe(kwargs.get('pk'))

        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            partial=True,
            many=False,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        recipe = self.get_recipe(kwargs.get('pk'))
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagApiV2Detail(APIView):
    def get(self, request, **kwargs):
        tag = get_object_or_404(Tag.objects.filter(pk=kwargs.get('pk')))
        serializer = TagSerializer(
            instance=tag,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
