import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Model

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


class Command(BaseCommand):
    help = 'Loads data from csv files'

    def handle(self, *args, **options) -> None:
        UsersLoader().read()
        CategoryLoader().read()
        GenreLoader().read()
        TitleLoader().read()
        GenreTitleLoader().read()
        ReviewLoader().read()
        CommentLoader().read()


class CsvLoader:
    def parse(self, data: dict[str, str]) -> Model:
        pass

    def get_file_name(self) -> str:
        assert isinstance(self.file_name, str), (
            "'%s' should either include a `file_name` attribute, "
            "or override the `get_file_name()` method."
            % self.__class__.__name__
        )
        return self.file_name

    def read(self) -> None:
        file_name = self.get_file_name()
        print(f'load data from {file_name}')
        with open(file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = self.parse(row)
                instance.save()


class UsersLoader(CsvLoader):
    file_name = 'static/data/users.csv'

    def parse(self, data: dict[str, str]) -> User:
        instance = User(
            id=int(data.get('id')),
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role'),
            bio=data.get('bio'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
        )
        return instance


class CategoryLoader(CsvLoader):
    file_name = 'static/data/category.csv'

    def parse(self, data: dict[str, str]) -> Category:
        instance = Category(
            id=int(data.get('id')),
            name=data.get('name'),
            slug=data.get('slug'),
        )
        return instance


class GenreLoader(CsvLoader):
    file_name = 'static/data/genre.csv'

    def parse(self, data: dict[str, str]) -> Genre:
        instance = Genre(
            id=int(data.get('id')),
            name=data.get('name'),
            slug=data.get('slug'),
        )
        return instance


class TitleLoader(CsvLoader):
    file_name = 'static/data/titles.csv'

    def parse(self, data: dict[str, str]) -> Title:
        instance = Title(
            id=int(data.get('id')),
            name=data.get('name'),
            year=int(data.get('year')),
            category_id=int(data.get('category')),
        )
        return instance


class GenreTitleLoader(CsvLoader):
    file_name = 'static/data/genre_title.csv'

    def parse(self, data: dict[str, str]) -> GenreTitle:
        instance = GenreTitle(
            id=int(data.get('id')),
            title_id=int(data.get('title_id')),
            genre_id=int(data.get('genre_id')),
        )
        return instance


class ReviewLoader(CsvLoader):
    file_name = 'static/data/review.csv'

    def parse(self, data: dict[str, str]) -> Review:
        instance = Review(
            id=int(data.get('id')),
            title_id=int(data.get('title_id')),
            text=data.get('text'),
            author_id=int(data.get('author')),
            score=int(data.get('score')),
            pub_date=datetime.strptime(
                data.get('pub_date'),
                '%Y-%m-%dT%H:%M:%S.%fZ',
            ),
        )
        return instance


class CommentLoader(CsvLoader):
    file_name = 'static/data/comments.csv'

    def parse(self, data: dict[str, str]) -> Comment:
        instance = Comment(
            id=int(data.get('id')),
            review_id=int(data.get('review_id')),
            text=data.get('text'),
            author_id=int(data.get('author')),
            pub_date=datetime.strptime(
                data.get('pub_date'),
                '%Y-%m-%dT%H:%M:%S.%fZ',
            ),
        )
        return instance
