from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product, ProductVariant
from apps.users.models import UserAddress
from apps.orders.models import Order, OrderItem, DeliverySlot
from .models import Cart, CartItem, Coupon


def _get_or_create_cart(request) -> Cart:
    """
    Retrieve the active cart for the current user or session,
    creating one if needed.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
    else:
        if not request.session.session_key:
            request.session.save()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, is_active=True)
    return cart


@require_POST
def add_to_cart(request):
    """
    AJAX endpoint for adding a product (and optional variant) to the cart.

    Expected POST data:
      - product_id (required)
      - variant_id (optional)
      - quantity (optional, defaults to 1)

    Returns JSON with cart item count and total so the UI can update instantly.
    """
    product_id = request.POST.get("product_id")
    variant_id = request.POST.get("variant_id")

    if not product_id:
        return JsonResponse({"ok": False, "error": "Missing product_id"}, status=400)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, quantity)

    product = get_object_or_404(Product, pk=product_id, is_available=True)
    variant = None
    if variant_id:
        variant = get_object_or_404(
            ProductVariant,
            pk=variant_id,
            product=product,
            is_active=True,
        )

    cart = _get_or_create_cart(request)

    with transaction.atomic():
        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={"quantity": 0, "unit_price": Decimal("0.00"), "total_price": Decimal("0.00")},
        )
        item.quantity += quantity
        item.save()  # CartItem.save() recalculates prices

    # Refresh aggregates
    cart.refresh_from_db()

    if request.headers.get("HX-Request"):
        return render(request, "components/cart_update_oob.html", {
            "cart": cart,
            "cart_items_count": cart.total_items,
            "message": f"Added {product.name} to cart"
        })

    return JsonResponse(
        {
            "ok": True,
            "message": f"Added {quantity} × {product.name} to your cart.",
            "cart_total": str(cart.total),
            "cart_count": cart.total_items,
            "item_id": item.id,
            "item_quantity": item.quantity,
        }
    )


def cart_view(request):
    """Display shopping cart"""
    cart = _get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'pages/cart/cart.html', context)


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        product_name = cart_item.product.name
        cart_item.delete()
        
        cart = _get_or_create_cart(request)
        cart.refresh_from_db()
        
        if request.headers.get('HX-Request'):
            return render(request, "components/cart_update_oob.html", {
                "cart": cart,
                "cart_items_count": cart.total_items,
                "message": f"Removed {product_name} from cart"
            })

        return JsonResponse({
            'success': True,
            'cart_total': str(cart.total),
            'cart_items': cart.total_items
        })
        
    except Exception as e:
        if request.headers.get('HX-Request'):
             return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def update_cart_item(request):
    """Update cart item quantity"""
    try:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
        
        cart = _get_or_create_cart(request)
        cart.refresh_from_db()
        
        return JsonResponse({
            'success': True,
            'item_total': str(cart_item.total_price),
            'cart_total': str(cart.total),
            'cart_items': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def checkout_view(request):
    """Checkout page"""
    cart = _get_or_create_cart(request)
    
    # Check if cart has items
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart:view')
    
    # Get user addresses
    addresses = UserAddress.objects.filter(user=request.user)
    
    # Get delivery slots
    delivery_slots = DeliverySlot.objects.filter(is_available=True)
    
    context = {
        'cart': cart,
        'addresses': addresses,
        'delivery_slots': delivery_slots,
    }
    return render(request, 'pages/cart/checkout.html', context)


@require_POST
@login_required
def apply_coupon(request):
    """Apply coupon to cart"""
    try:
        coupon_code = request.POST.get('coupon_code')
        cart = _get_or_create_cart(request)
        
        coupon = get_object_or_404(Coupon, code=coupon_code.upper())
        
        if not coupon.is_valid:
            return JsonResponse({
                'success': False,
                'message': 'This coupon is no longer valid'
            })
        
        if not coupon.can_be_applied(float(cart.subtotal)):
            return JsonResponse({
                'success': False,
                'message': f'Minimum order value is ₹{coupon.minimum_order_value}'
            })
        
        cart.coupon_code = coupon_code
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Coupon {coupon_code} applied successfully!',
            'discount': str(coupon.calculate_discount(float(cart.subtotal))),
            'new_total': str(cart.total)
        })
        
    except Coupon.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid coupon code'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@transaction.atomic
def process_checkout(request):
    """Process checkout and create order"""
    if request.method != 'POST':
        return redirect('cart:checkout')
    
    cart = _get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart:view')
    
    try:
        # Get form data
        address_id = request.POST.get('address_id')
        delivery_date = request.POST.get('delivery_date')
        delivery_slot = request.POST.get('delivery_slot')
        gift_message = request.POST.get('gift_message', '')
        special_instructions = request.POST.get('special_instructions', '')
        payment_method = request.POST.get('payment_method', 'card')
        
        # Validate required fields
        if not all([address_id, delivery_date, delivery_slot]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('cart:checkout')
        
        # Get address
        address = get_object_or_404(UserAddress, id=address_id, user=request.user)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            status='pending',
            payment_status='pending',
            subtotal=cart.subtotal,
            discount_amount=cart.total_discount,
            total_amount=cart.total,
            customer_name=address.full_name,
            customer_email=request.user.email,
            customer_phone=address.phone_number,
            delivery_address=f"{address.street_address}, {address.landmark}",
            delivery_city=address.city,
            delivery_state=address.state,
            delivery_postal_code=address.postal_code,
            delivery_country=address.country,
            preferred_delivery_date=delivery_date,
            preferred_delivery_slot=delivery_slot,
            gift_message=gift_message,
            special_instructions=special_instructions,
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.slug,
                product_weight=cart_item.product.weight,
            )
        
        # Clear cart
        cart.items.all().delete()
        cart.is_active = False
        cart.save()
        
        if payment_method == 'cod':
            messages.success(request, f'Order #{order.order_number} placed successfully!')
            return redirect('orders:detail', order_id=order.id)
        else:
            # Redirect to demo payment gateway
            return redirect('payments:demo', order_id=order.id)
            
    except Exception as e:
        messages.error(request, f'Error processing order: {str(e)}')
        return redirect('cart:checkout')