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
    path('wishlist/', views.wishlist, name="wishlist"),
    #path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name="remove_from_wishlist"),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


    # Add stuff
    path('edit_category/', views.edit_category, name="edit_category"),

]
