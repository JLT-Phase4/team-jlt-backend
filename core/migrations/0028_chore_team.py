# Generated by Django 3.1.7 on 2021-02-23 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20210223_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.team'),
        ),
    ]
