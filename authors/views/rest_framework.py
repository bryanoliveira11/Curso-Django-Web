from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..serializers import AuthorSerializer


class AuthorApiV2Pagination(PageNumberPagination):
    page_size = 9


class AuthorsApiV2ViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    pagination_class = AuthorApiV2Pagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(
            username=self.request.user.username  # type:ignore
        )
        return qs

    @action(
        methods=['get'],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj
        )
        return Response(serializer.data)
