from typing import OrderedDict, Union

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from api.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser, validate_user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, value: OrderedDict) -> OrderedDict:
        if self.context.get(
            'request',
        ).method == 'POST' and Review.objects.filter(
            title__reviews__author=self.context.get('request').user,
        ):
            raise serializers.ValidationError(
                'Ваш отзыв на это произведение уже существует.',
            )
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'rating',
            'category',
            'genre',
        )

    def get_rating(self, title: Title) -> Union[int, None]:
        rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        return None if rating is None else round(rating)


class TitleWriteSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_blank=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
            validate_user,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
            validate_user,
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code',
        )


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=False,
    )
    email = serializers.EmailField(
        max_length=254,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=False,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=False,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username,
        ],
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
