from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Customers
class Customer(AbstractUser):
    username = models.CharField(max_length=100, null=False, unique=True, default=" ")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.username} '


# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)


    # Allows it to show in the django admin as such
    def __str__(self):
        return self.name
    
    # To fix django's pluralising of models
    class Meta:
        verbose_name_plural = 'categories'

    #def get_absolute_url(self):
	    #return reverse('home')


# All products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    # For Product Sale 
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return f'{self.name} | {self.category}'
    
    def add_to_wishlist(self, user):
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        wishlist.products.add(self)

# Wishlist
class Wishlist(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f'Wishlist for {self.user.username}'


# Was not implemented
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    #status = models.BooleanField(default=False)

    def __str__(self):
        return {self.product}