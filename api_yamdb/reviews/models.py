from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Comment(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text[20:]}[...] - {self.author}@{self.pub_date}'


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        "Title", on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text[20:]}[...] - {self.author}@{self.pub_date}'
