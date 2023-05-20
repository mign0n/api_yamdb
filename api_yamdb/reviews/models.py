from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class PubDateModel(models.Model):
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория произведений'
        verbose_name_plural = 'Категории произведений'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год создания произведения',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    category = models.ForeignKey(
        verbose_name='Категория произведения',
        to='Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        verbose_name='Произведение',
        to=Title,
        on_delete=models.CASCADE,
        related_name='genres',
    )
    genre = models.ForeignKey(
        verbose_name='Жанр',
        to=Genre,
        on_delete=models.CASCADE,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'genre'),
                name='unique_genre_title',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.title} - {self.genre}'


class Review(PubDateModel):
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.ForeignKey(
        verbose_name='Произведение',
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        verbose_name='Автор отзыва',
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв на произведение'
        verbose_name_plural = 'Отзывы на произведения'
        constraints = [
            models.UniqueConstraint(
                fields=('title_id', 'author_id'),
                name='unique_title_author',
            ),
        ]

    def __str__(self) -> str:
        return self.text


class Comment(PubDateModel):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    review = models.ForeignKey(
        verbose_name='Отзыв на произведение',
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        verbose_name='Автор комментария',
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву на произведение'
        verbose_name_plural = 'Комментарии к отзывам на произведения'

    def __str__(self) -> str:
        return self.text
