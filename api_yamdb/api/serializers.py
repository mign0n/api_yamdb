import re
from typing import Union

from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


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
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        match = re.fullmatch(settings.USERNAME_PATTERN_REGEX, value)
        if not match:
            raise serializers.ValidationError('Имя пользователя некорректно.')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code',
        )

class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    email = serializers.EmailField(max_length=254,
                                   required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                    'last_name', 'bio', 'role',)

    def validate_username(self, value):

        match = re.fullmatch(settings.USERNAME_PATTERN_REGEX, value)
        if not match:
            raise serializers.ValidationError(
                'Имя пользователя некорректно.'
            )
        return value


class UsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     required=False)
    email = serializers.EmailField(max_length=254,
                                   required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                    'last_name', 'bio', 'role',)


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     required=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    email = serializers.EmailField(max_length=254,
                                   required=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    def validate_username(self, value):

        match = re.fullmatch(settings.USERNAME_PATTERN_REGEX, value)
        if not match:
            raise serializers.ValidationError(
                'Имя пользователя некорректно.'
            )
        return value
