from django.shortcuts import redirect, render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {'products': products, 'categories': categories}
    return render(request, 'store/home.html', context)

def about(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'store/about.html', context)

# Authentication functions

def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have successfuly registered and logged in!"))
            return redirect('home') 
        else:
            messages.success(request, ("There was an issue registering. Please try again."))
            return redirect('register')
    else:
        context = {'form': form}
        return render(request, 'store/register.html', context)
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("You have logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error when logging in. Please try again."))
            return redirect('login')

    else:
        context = {}
        return render(request, 'store/login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out sucessfully!"))
    return redirect('home')


# Product functions

def product(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)

    context = {'product': product, 'categories': categories}
    return render(request, 'store/product.html', context)

def category(request,  var):
    categories = Category.objects.all()
    # Replace hyphens with spaces
    print(f"{var}")
    var = var.replace('-', ' ')

    # Grab category from url
    try:
        #category = Category.objects.get(name=var)
        category = Category.objects.get(name__iexact=var)
        print(f"Found category: {category.name}")
        
        products = Product.objects.filter(category=category)
        print(f"Found products: {products}")

        context = {'products': products, 'category': category, 'categories': categories}
        return render(request, 'store/category.html', context)
    except Category.DoesNotExist:
        print(f"Exception {categories}")
        messages.success(request, ("That category does not exist."))
        return redirect('home')



def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
