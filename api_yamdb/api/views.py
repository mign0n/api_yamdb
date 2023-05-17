from django.db.models import QuerySet
from django.utils.functional import cached_property
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Comment, Genre, GenreTitle, Title


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

    @cached_property
    def _title(self) -> QuerySet:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        return self._title.reviews.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
