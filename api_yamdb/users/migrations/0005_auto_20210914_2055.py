# Generated by Django 2.2.16 on 2021-09-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210914_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('user', 'юзер'), ('moderator', 'модераторв'), ('admin', 'админ')], editable=False, verbose_name='Роль'),
        ),
    ]