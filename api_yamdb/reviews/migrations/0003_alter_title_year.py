# Generated by Django 3.2 on 2024-06-24 08:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20231210_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(error_messages={'validators': 'Значение года не может быть больше текущего и меньше 0!'}, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2024)], verbose_name='Год выпуска'),
        ),
    ]
