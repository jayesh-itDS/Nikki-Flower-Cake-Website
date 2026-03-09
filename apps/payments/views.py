from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.orders.models import Order

@login_required
def payment_demo_view(request, order_id):
    """
    Simulated payment gateway screen.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user, payment_status='pending')
    
    context = {
        'order': order,
    }
    return render(request, 'pages/payments/demo.html', context)


@login_required
def process_payment_view(request, order_id):
    """
    Process the mock payment and update order status.
    """
    if request.method != 'POST':
        return redirect('payments:demo', order_id=order_id)
        
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Simulate successful payment
    order.payment_status = 'completed'
    order.save()
    
    messages.success(request, f'Payment successful! Order #{order.order_number} is confirmed.')
    return redirect('orders:detail', order_id=order.id)