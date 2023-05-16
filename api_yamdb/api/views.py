from rest_framework import filters, viewsets

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreTitleViewSet(viewsets.ModelViewSet):
    serializer_class = GenreTitleSerializer
    queryset = GenreTitle.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
