# Generated by Django 3.1.7 on 2021-03-06 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_auto_20210303_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='published',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
