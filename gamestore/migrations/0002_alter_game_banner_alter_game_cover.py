# Generated by Django 4.0.4 on 2022-05-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='banner',
            field=models.ImageField(upload_to='banners'),
        ),
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(upload_to='covers'),
        ),
    ]
