# Generated by Django 5.2 on 2025-04-21 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beautytipcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
