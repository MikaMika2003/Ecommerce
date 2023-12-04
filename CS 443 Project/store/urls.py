from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    # Authentication
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    # Products
    path('product/<int:pk>/', views.product, name="product"),
    path('edit_product/', views.edit_product, name='edit_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product_edit'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),

    # Categories
    path('category/<str:var>/', views.category, name="category"),

    # Wishlist
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


    # Add stuff
    path('edit_category/', views.edit_category, name="edit_category"),

]
