# Generated by Django 4.0.4 on 2022-05-16 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0008_remove_customer_wishlist_customer_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profilePictures'),
        ),
    ]
