from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUpView,
    TitleViewSet,
    TokenView,
    UserMeViewSet,
    UsernameViewSet,
    UsersViewSet,
)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
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
    path('v1/users/me/',
         UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'update'}),
         name='user_me'),
    path('v1/users/<str:username>/',
         UsernameViewSet.as_view(
             {'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='username'),
    path('v1/users/',
         UsersViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='users'),
]
