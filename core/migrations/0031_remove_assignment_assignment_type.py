# Generated by Django 3.1.7 on 2021-02-24 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20210224_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='assignment_type',
        ),
    ]
