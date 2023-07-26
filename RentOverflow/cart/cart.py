from decimal import Decimal 
from store.models import Property 
import math
import copy 
class Cart():
    def __init__(self, request):
        self.session = request.session
        # Returning user - obtain his/her existing session
        cart = self.session.get('session_key')
        # New user - generate a new session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def update(self, property_id):
        property_id = str(property_id)
        if property_id in self.cart:
            del self.cart[property_id]
        else:
            self.cart[property_id] = 1
        self.session.modified = True
