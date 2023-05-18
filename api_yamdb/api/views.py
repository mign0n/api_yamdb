import random

from django.core.mail import send_mail
from django.db.models import QuerySet
from django.utils.functional import cached_property
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenSerializer,
)
from reviews.models import Category, Comment, Genre, GenreTitle, Title
from users.models import CustomUser


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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cached_property
    def _title(self) -> QuerySet:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        return self._title.reviews.all()

    def create(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict,
    ) -> Response:
        request.data['author'] = self.request.user.pk
        request.data['title'] = self.kwargs.get('title_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


class SignUpView(APIView):
    """Отправка письма с кодом подтверждения на email."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        try:
            user = CustomUser.objects.get(
                username=request.data.get('username'),
            )
            code = getattr(user, 'confirmation_code')
            email = getattr(user, 'email')
            if not code and user or code and user:
                if request.data.get('email') != email:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                confirmation_code = random.randint(00000, 99999)
                send_mail(
                    'Код подтверждения регистрации',
                    'Вы зарегистрированы на YAMDB!'
                    f' Ваш код подтвержения: {confirmation_code}',
                    'admin@yamdb.com',
                    [email],
                    fail_silently=False,
                )
                user.confirmation_code = confirmation_code
                user.save()
                return Response(status=status.HTTP_200_OK)
        except:
            pass
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = random.randint(00000, 99999)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'Код подтверждения регистрации',
            'Вы зарегистрированы на YAMDB!'
            f' Ваш код подтвержения: {confirmation_code}',
            'admin@yamdb.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Получение JWT-токена в обмен на username и confirmation code."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = serializer.data['username']
        user = get_object_or_404(CustomUser, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if user.confirmation_code != confirmation_code:
            return Response(
                {'Код подтверждения не верен'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
