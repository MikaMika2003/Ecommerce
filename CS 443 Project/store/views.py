from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Category, Wishlist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, WishlistForm, ProductForm
from django import forms
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='home')
def edit_category(request):
    # Get list of categories
    categories = Category.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'add':
            name = request.POST.get('name', None)
            if name:
                Category.objects.create(name=name)
        elif action == 'update':
            category_id = request.POST.get('category_id', None)
            name = request.POST.get('name', None)
            if category_id and name:
                category = get_object_or_404(Category, pk=category_id)
                category.name = name
                category.save()
        elif action == 'delete':
            category_id = request.POST.get('category_id', None)
            if category_id:
                category = get_object_or_404(Category, pk=category_id)
                category.delete()

        messages.success(request, ("Changes have been made successfully."))
        return redirect('edit_category')

    context = {'categories': categories}
    return render(request, 'store/edit_category.html', context)

@login_required(login_url='home')
def edit_product(request, product_id=None):
    # Get list of categories for rendering the form
    categories = Category.objects.all()
    products = Product.objects.all()

    if product_id:
        # Editing an existing product
        product = get_object_or_404(Product, pk=product_id)
    else:
        # Adding a new product
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product saved successfully.")
            return redirect('edit_product')
        else:
            messages.error(request, "Error saving the product. Please check the form.")
    else:
        form = ProductForm(instance=product)

    context = {'form': form, 'categories': categories, 'products': products}
    return render(request, 'store/edit_product.html', context)

@login_required(login_url='home')
def update_product(request, product_id):
    # Get the existing product to update
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Process the form data when the user submits the update form
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('edit_product')  # Redirect to the product list or wherever you want
        else:
            messages.error(request, "Error updating the product. Please check the form.")
    else:
        # Display the form to the user with the existing product data
        form = ProductForm(instance=product)

    context = {'form': form, 'product': product}
    return render(request, 'store/update_product.html', context)

@login_required(login_url='home')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('edit_product')

@login_required(login_url='home')
def wishlist(request):
    categories = Category.objects.all()
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            wishlist.products.add(product)
            return redirect('wishlist')
    else:
        form = WishlistForm()

    context = {'wishlist': wishlist, 'form': form, 'categories': categories}
    return render(request, 'store/wishlist.html', context)

@login_required(login_url='home')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.add_to_wishlist(request.user)
    return redirect('wishlist')

@login_required(login_url='home')
def remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    return redirect('wishlist')