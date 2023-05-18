import re

from django.conf import settings
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTitle
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


    def validate_username(self, value):

        match = re.fullmatch(settings.USERNAME_PATTERN_REGEX, value)
        if not match:
            raise serializers.ValidationError(
                'Имя пользователя некорректно.'
            )
        return value

class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code',)
