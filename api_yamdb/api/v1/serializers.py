from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.fields import IntegerField
from rest_framework.response import Response
from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, CharField, EmailField
)
from rest_framework.validators import (
    UniqueValidator, ValidationError
)
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Review, Title, Category, Comment, Genre
)
from users.models import User
from .validators import validator_username, validate_me
from api_yamdb.settings import (
    EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH, CONFIRMATION_CODE_MAX_LENGTH
)


class AddUserSerializer(ModelSerializer):
    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        required=True,
    )
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            validate_me,
            validator_username,
        ),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class GetUserTokenSerializer(ModelSerializer):
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class UserSerializer(ModelSerializer):
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            validator_username,
            UniqueValidator(
                User.objects.all()
            ),
        ),
    )
    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        required=True,
        validators=(
            UniqueValidator(
                User.objects.all()
            ),
        ),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ReviewSerializer(ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title,
                author=author,
            ).exists()
        ):
            raise ValidationError(
                'Вы можете оставить только 1 отзыв!'
            )
        return data


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'category',
            'description',
            'genre',
            'name',
            'year',
        )


class GetTitleSerializer(ModelSerializer):
    rating = IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
    )
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'category',
            'description',
            'genre',
            'name',
            'year',
            'rating',
        )


class CommentSerializer(ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
