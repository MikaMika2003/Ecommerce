from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    return render(request, "cart_summary.html")

def cart_add(request):
	# Get the cart
	cart = Cart(request)
     
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)

		# Save to session
		cart.add(product=product)

		# Return resonse
		response = JsonResponse({'Product Name: ': product.name})
		return response
     
def cart_add(request):
    # Get cart
    cart = Cart(request)
    
    # test if POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))

        # lookup product in database
        product = get_object_or_404(Product, id=product_id)
        print(f'product: {product}')

        # Save to a session
        cart.add(product=product)

        # Return response
        response_data = ({'Product Name': product.name})

        return JsonResponse(response_data)
    pass


def cart_delete(request):
    pass

def cart_update(request):
    pass