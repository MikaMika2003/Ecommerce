from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    # Authentication
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    # Products and such
    path('product/<int:pk>/', views.product, name="product"),
    path('category/<str:var>/', views.category, name="category"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
]
