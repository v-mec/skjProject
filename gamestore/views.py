from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gamestore.forms import CustomerForm, UserForm
from gamestore.models import Category, Game, Customer, Order, Review, Comment


def index(request):
    category_list = Category.objects.all()
    game_list = Game.objects.all().order_by('name')
    recent_game_list = Game.objects.all().order_by('-id')[:5]
    return render(request, 'gamestore/index.html',
                  {'category_list': category_list, 'recent_game_list': recent_game_list, 'game_list': game_list})


def game(request, game_id):
    game_ = get_object_or_404(Game, pk=game_id)
    if request.user.is_authenticated:
        reviews = Review.objects.filter(game=game_).exclude(user=request.user)
    else:
        reviews = Review.objects.filter(game=game_)

    try:
        user_review = Review.objects.get(game=game_, user=request.user)
    except (Review.DoesNotExist, TypeError):
        user_review = None

    if request.method == 'POST':
        if 'postReview' in request.POST:
            text = request.POST['text']
            recommend = request.POST['recommend'] == '1'
            if user_review:
                user_review.text = text
                user_review.recommend = recommend
                user_review.save()
            else:
                user_review = Review(user=request.user, game=game_, text=text, recommend=recommend)
                user_review.save()
        elif 'deleteReview' in request.POST:
            user_review.delete()
            user_review = None
        else:
            request.user.customer.cart.add(game_)

    error_message = None
    can_write_review = False
    if not request.user.is_authenticated:
        error_message = 'You must be logged in'
    elif request.user.customer.cart.contains(game_):
        error_message = 'Already in cart'
    elif request.user.customer.library.contains(game_):
        error_message = 'Already in library'
        can_write_review = True

    return render(request, 'gamestore/game.html', {'game': game_, 'error_message': error_message,
                                                   'can_write_review': can_write_review, 'user_review': user_review,
                                                   'reviews': reviews})


def category(request, category_id):
    category_ = get_object_or_404(Category, pk=category_id)
    game_list = Game.objects.filter(category=category_)
    return render(request, 'gamestore/category.html', {'category': category_, 'game_list': game_list})


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        error = 'Invalid username or password'

    return render(request, 'gamestore/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            error = 'User with this username already exists'
        else:
            u = User.objects.create_user(username=username, password=password)
            u.save()
            c = Customer(user=u)
            c.save()
            return HttpResponseRedirect('/login')

    return render(request, 'gamestore/register.html', {'error': error})


@login_required
def cart(request):
    if request.method == 'POST':
        game_id = request.POST['game_id']
        g = Game.objects.get(pk=game_id)
        request.user.customer.cart.remove(g)

    cart_game_list = Game.objects.filter(cart_customers__user=request.user)
    total_price = cart_game_list.aggregate(Sum('price'))['price__sum']
    if total_price is not None:
        total_price = round(total_price, 2)
    return render(request, 'gamestore/cart.html', {'cart_game_list': cart_game_list, 'total_price': total_price})


@login_required
def order(request):
    if request.method == 'POST':
        user_cart = request.user.customer.cart.all()
        total_price = user_cart.aggregate(Sum('price'))['price__sum']
        order_ = Order(user=request.user, price=total_price)
        order_.save()
        order_.games.add(*user_cart)
        request.user.customer.library.add(*user_cart)
        request.user.customer.cart.clear()
        return render(request, 'gamestore/orderProcess.html')

    return render(request, 'gamestore/order.html')


def profile(request, user_id):
    user_ = get_object_or_404(User, pk=user_id)
    user_games = Game.objects.filter(library_customers__user_id=user_id)
    user_reviews = Review.objects.filter(user_id=user_id)
    return render(request, 'gamestore/profile.html', {'user': user_, 'user_games': user_games})


def review(request, review_id):
    if request.method == 'POST':
        if 'deleteComment' in request.POST:
            comment_id = request.POST['deleteComment']
            Comment.objects.get(pk=comment_id).delete()
        else:
            text = request.POST['text']
            c = Comment(user=request.user, review_id=review_id, text=text)
            c.save()

    review_ = get_object_or_404(Review, pk=review_id)
    comments = review_.comment_set.all()
    return render(request, 'gamestore/review.html', {'review': review_, 'comments': comments})


@login_required
def orders(request):
    orders_ = Order.objects.filter(user=request.user)
    return render(request, 'gamestore/orders.html', {'orders': orders_})


@login_required
def profile_edit(request):
    u = request.user
    if request.method == 'POST':
        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.customer.about = request.POST['about']
        u.save()
        u.customer.save()

    customer_form = CustomerForm(instance=u.customer)
    user_form = UserForm(instance=u)
    return render(request, 'gamestore/profileEdit.html', {'customer_form': customer_form, 'user_form': user_form})


def search(request):
    query = request.GET['query']
    game_list = Game.objects.filter(name__contains=query)
    return render(request, 'gamestore/search.html', {'game_list': game_list, 'query': query})
