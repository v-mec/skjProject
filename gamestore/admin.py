from django.contrib import admin

from gamestore.models import Category, Game, Customer, Order, Review, Comment

admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Comment)
