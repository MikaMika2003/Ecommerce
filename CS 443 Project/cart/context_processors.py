from .cart import Cart

# Create context processor to let cart work on all pages
def cart(request):

    
    # Return default data of cart
    return {'cart': Cart(request)}