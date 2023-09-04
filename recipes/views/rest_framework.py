from django.shortcuts import get_object_or_404
from rest_framework import status
# from rest_framework.generics import (ListCreateAPIView,
#                                      RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Recipe
from ..permissions import IsOwner
from ..serializers import RecipeSerializer, TagSerializer


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = 9


# class for get (list or detail), patch, post, delete
class RecipeApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()  # type:ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get(  # type:ignore
            'category_id', ''
        )
        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def create(self, request, *args, **kwargs):  # POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(),]

        return super().get_permissions()


# class RecipeApiV2List(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()  # type:ignore
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeApiV2Pagination

#     # def get(self, request):
#     #      recipes = Recipe.objects.get_published()[:10]  # type:ignore
#     #      serializer = RecipeSerializer(
#     #          instance=recipes,
#     #          many=True,
#     #          context={'request': request},
#     #      )
#     #      return Response(serializer.data)

#     # def post(self, request):
#     #      serializer = RecipeSerializer(
#     #          data=request.data, context={'request': request},
#     #      )
#     #      serializer.is_valid(raise_exception=True)
#     #      serializer.save(
#     #          author_id=1, category_id=2,
#     #          tags=[1, 2]
#     #      )
#     #      return Response(
#     #          serializer.data,
#     #          status=status.HTTP_201_CREATED,
#     #      )


# class RecipeApiV2Detail(RetrieveUpdateDestroyAPIView):
    # queryset = Recipe.objects.get_published()  # type:ignore
    # serializer_class = RecipeSerializer
    # pagination_class = RecipeApiV2Pagination

    # def get_recipe(self, pk):
    #     return get_object_or_404(
    #         Recipe.objects.get_published(), pk=pk  # type:ignore
    #     )

    # def get(self, request, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))

    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         many=False,
    #         context={'request': request},
    #     )
    #     return Response(serializer.data)

    # def patch(self, request, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))

    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         data=request.data,
    #         partial=True,
    #         many=False,
    #         context={'request': request},
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def delete(self, request, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class TagApiV2Detail(APIView):
    def get(self, request, **kwargs):
        tag = get_object_or_404(Tag.objects.filter(pk=kwargs.get('pk')))
        serializer = TagSerializer(
            instance=tag,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
