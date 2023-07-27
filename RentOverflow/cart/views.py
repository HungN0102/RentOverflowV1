from django.shortcuts import render
from .cart import Cart 
from store.models import Property
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart_summary.html', {'cart':cart})

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        property_id = int(request.POST.get('property_id'))
        cart.update(product=property_id)

        response = JsonResponse({
            'msg': 'this is a success'
        })
    return response