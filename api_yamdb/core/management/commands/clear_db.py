from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


class Command(BaseCommand):

    help = 'Clear database'

    def handle(self, *args, **options) -> None:
        Comment.objects.all().delete()
        Review.objects.all().delete()
        GenreTitle.objects.all().delete()
        Title.objects.all().delete()
        Genre.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False)
