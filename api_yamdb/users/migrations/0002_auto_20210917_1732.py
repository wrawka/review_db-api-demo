# Generated by Django 2.2.16 on 2021-09-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='confirmation_code',
            field=models.TextField(verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.TextField(blank=True, null=True, verbose_name='Code'),
        ),
    ]