from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GenreTitleViewSet, ReviewViewSet, TitleViewSet)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('comments', CommentViewSet, basename='comment')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('genretitle', GenreTitleViewSet, basename='genre-title')
v1_router.register('reviews', ReviewViewSet, basename='review')
v1_router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
