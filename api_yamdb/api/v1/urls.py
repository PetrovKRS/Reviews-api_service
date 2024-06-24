from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ReviewViewSet, CommentViewSet, TitleViewSet,
    GenreViewSet, CategoryViewSet, AddUserViewSet,
    GetUserTokenViewSet, UserViewSet,
)

router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = (
    path(
        'auth/signup/',
        AddUserViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'auth/token/',
        GetUserTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
    path(
        '',
        include(router.urls)
    ),
)
