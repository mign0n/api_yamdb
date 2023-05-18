from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreTitleViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

from api.views import SignUpView, TokenView

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('genretitle', GenreTitleViewSet, basename='genre-title')
v1_router.register('titles', TitleViewSet, basename='title')

v1_reviews_router = SimpleRouter()
v1_reviews_router.register('reviews', ReviewViewSet, basename='review')

v1_comments_router = SimpleRouter()
v1_comments_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/titles/<int:title_id>/', include(v1_reviews_router.urls)),
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/',
        include(v1_comments_router.urls),
    ),
    path('v1/auth/signup/', SignUpView.as_view(), name='register_user'),
    path('v1/auth/token/', TokenView.as_view(), name='token_create'),
]
