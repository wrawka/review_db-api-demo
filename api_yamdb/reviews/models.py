from django.db import models
from django.core.validators import RegexValidator



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
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        null=True,
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
