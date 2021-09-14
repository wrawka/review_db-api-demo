# Generated by Django 2.2.16 on 2021-09-14 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20210914_2213'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='single_review_per_title'),
        ),
    ]