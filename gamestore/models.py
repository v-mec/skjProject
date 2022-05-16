from django.contrib.auth.models import User
from django.db import models

from skjProject import settings


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Game(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers')
    banner = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    cart = models.ManyToManyField(Game, related_name='cart_customers', blank=True)
    library = models.ManyToManyField(Game, related_name='library_customers', blank=True)
    # profile_picture = models.ImageField(upload_to='profilePictures', blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    recommend = models.BooleanField()
    text = models.TextField()


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
