# Generated by Django 2.2.16 on 2021-09-14 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210914_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('user', 'юзер'), ('moderator', 'модераторв'), ('admin', 'админ')], default='user', verbose_name='Роль'),
        ),
    ]
