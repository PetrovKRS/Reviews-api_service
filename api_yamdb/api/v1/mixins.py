from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin,
    DestroyModelMixin
)


class ListCreateDestroyMixin(
    CreateModelMixin, ListModelMixin,
    DestroyModelMixin, viewsets.GenericViewSet,
):
    pass
