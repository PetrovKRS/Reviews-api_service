from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Title, Genre, Category
)
from users.models import User

from .serializers import (
    ReviewSerializer, CommentSerializer, GenreSerializer,
    CategorySerializer, GetTitleSerializer, TitleSerializer,
    AddUserSerializer, UserSerializer, GetUserTokenSerializer,
)
from .filters import TitleFilter
from .permissions import (
    AdminOrReadOnlyPermission, ReadOnlyPermission,
    AdminModerAuthorUserOrReadOnly, AdminSuperPermission
)
from .mixins import ListCreateDestroyMixin
from api_yamdb.settings import EMAIL_HOST_USER


class AddUserViewSet(viewsets.ModelViewSet):
    """ Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена. Использовать имя
    'me' в качестве username запрещено. Поля email и
    username должны быть уникальными. Должна быть возможность
    повторного запроса кода подтверждения.
    """

    queryset = User.objects.all()
    serializer_class = AddUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def create(self, request, *args, **kwargs):
        """ Высылаем код подтверждения, для получения токена,
        на почту пользователя!
        """
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код для регистрации пользователя!',
            f'Код подтверждения: {confirmation_code}',
            EMAIL_HOST_USER,
            (user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserTokenViewSet(viewsets.ModelViewSet):
    """ Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """
    queryset = User.objects.all()
    serializer_class = GetUserTokenSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def create(self, request, **kwargs):
        serializer = GetUserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {"token": str(token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ Работа с пользователями. Права доступа: Администратор. """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminSuperPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated | IsAdminUser,),
        url_path='me',
    )
    def edit_profile(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username
        )
        if request.method == 'PATCH':
            serializer = UserSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyMixin):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyMixin):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().annotate(
            Avg('reviews__score')
        ).order_by('name')
    )
    serializer_class = TitleSerializer
    permission_classes = (
        ReadOnlyPermission
        | AdminOrReadOnlyPermission,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (
        AdminModerAuthorUserOrReadOnly,
    )
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def title(self):
        return (
            get_object_or_404(
                Title,
                id=self.kwargs.get('title_id')
            )
        )

    def review(self):
        return (
            get_object_or_404(
                self.title().reviews,
                id=self.kwargs.get('review_id')
            )
        )

    def get_queryset(self):
        return self.review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review()
        )


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (
        AdminModerAuthorUserOrReadOnly,
    )
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def title(self):
        return (
            get_object_or_404(
                Title,
                id=self.kwargs.get('title_id')
            )
        )

    def get_queryset(self):
        return self.title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title()
        )
