# Generated by Django 3.1.7 on 2021-02-23 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_chore_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='date',
        ),
    ]
