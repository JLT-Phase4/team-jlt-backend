# Generated by Django 3.1.7 on 2021-02-23 18:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210223_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='points',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
