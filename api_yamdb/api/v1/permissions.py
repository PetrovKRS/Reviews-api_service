from rest_framework.permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
)


class ReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AdminModerAuthorUserOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
            )
        )


class AdminOrReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin
                    or request.user.is_superuser
                )
            )
        )


class AdminSuperPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )
