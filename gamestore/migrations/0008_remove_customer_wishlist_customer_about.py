# Generated by Django 4.0.4 on 2022-05-15 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0007_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='customer',
            name='about',
            field=models.TextField(blank=True),
        ),
    ]
