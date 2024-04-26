from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Profile,Category,Cart
import random

# Create your views here.
def index(request):
    return render(request, 'index.html')

def pcbuild(request):
    products = Product.objects.all()
    return render(request, 'pcbuild.html',{'products': products})

def product_list(request):
    # Fetch all products
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "successful login...")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")
    else:
        return render(request, "login.html", {})
    
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")

def modal(request):
    products = Product.objects.all()
    return render(request, 'modal.html', {'products': products})


def register(request):
    if request.method == 'POST':
        # Get the form data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Attempt to create the user and profile
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile(user=user, phone=phone, address=address)
            profile.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed. {str(e)}')

    return render(request, 'signUp.html')


def category_list(request):
    categories = Category.objects.all()
    category_data = []
    for category in categories:
        items = Product.objects.filter(category=category)
        if items.exists():
            random_item = random.choice(items)
            category_data.append({'category': category, 'image': random_item.image})
    return render(request, 'categories.html', {'category_data': category_data})

def product_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {'category': category, 'products': products})


def add_to_cart(request, product_id):
    if request.user.is_authenticated:   
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1, 'price': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('view_cart')
        messages.success(request,'Item added to cart.')
    else:
        messages.error(request,'Please login to continue.')
        return redirect('login')



def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
    
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')