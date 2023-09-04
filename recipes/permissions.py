from rest_framework import permissions


class IsOwner(permissions.BasePermission):  # validating if user is owner of the recipe
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
