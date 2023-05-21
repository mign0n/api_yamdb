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

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

reviews_router = SimpleRouter()
reviews_router.register('reviews', ReviewViewSet, basename='review')

comments_router = SimpleRouter()
comments_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(reviews_router.urls)),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/',
        include(comments_router.urls),
    ),
    path('auth/signup/', SignUpView.as_view(), name='register_user'),
    path('auth/token/', TokenView.as_view(), name='token_create'),
    path('users/me/',
         UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'update'}),
         name='user_me'),
    path('users/<str:username>/',
         UsernameViewSet.as_view(
             {'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='username'),
    path('users/',
         UsersViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='users'),
]
