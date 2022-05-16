from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<int:game_id>/', views.game, name='game'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('review/<int:review_id>/', views.review, name='review'),
    path('orders', views.orders, name='orders'),
    path('search', views.search, name='search'),
]
