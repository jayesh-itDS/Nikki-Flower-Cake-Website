from .views import _get_or_create_cart

def cart_context(request):
    """
    Context processor to make the current cart and its item count 
    available to all templates.
    """
    cart = _get_or_create_cart(request)
    return {
        'cart': cart,
        'cart_items_count': cart.total_items if cart else 0
    }
