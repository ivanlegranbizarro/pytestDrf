# Generated by Django 4.2 on 2023-05-02 14:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("classroom", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="username",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
