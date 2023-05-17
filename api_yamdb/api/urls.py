from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import SignUpView, TokenView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='register_user'),
    path('v1/auth/token/', TokenView.as_view(), name='token_create'),
]
