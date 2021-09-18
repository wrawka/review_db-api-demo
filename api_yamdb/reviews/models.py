from textwrap import shorten
import datetime as dt
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import User


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True)

    def __str__(self) -> str:
        return f'{shorten(self.text)} - {self.author}@{self.pub_date}'


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        "Title", on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='single_review_per_title')
        ]

    def __str__(self) -> str:
        return f'{shorten(self.text)} - {self.author}@{self.pub_date}'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Только буквы и цифры!'
            )
        ]
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField(
        validators=[MaxValueValidator(dt.datetime.now().year)]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL,)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL,)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'genre']),
        ]
