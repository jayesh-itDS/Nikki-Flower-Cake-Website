from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.users.models import User
from apps.products.models import Product, ProductVariant
from apps.cart.models import Coupon


class Order(BaseModel):
    """
    Main order model.
    """
    ORDER_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(_('Order Number'), max_length=20, unique=True)
    status = models.CharField(_('Status'), max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('Payment Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Pricing
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('Tax Amount'), max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(_('Shipping Cost'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('Discount Amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Total Amount'), max_digits=10, decimal_places=2)
    
    # Coupon
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Customer information
    customer_name = models.CharField(_('Customer Name'), max_length=200)
    customer_email = models.EmailField(_('Customer Email'))
    customer_phone = models.CharField(_('Customer Phone'), max_length=15)
    
    # Delivery information
    delivery_address = models.TextField(_('Delivery Address'))
    delivery_landmark = models.CharField(_('Landmark'), max_length=255, blank=True)
    delivery_city = models.CharField(_('City'), max_length=100)
    delivery_state = models.CharField(_('State'), max_length=100)
    delivery_postal_code = models.CharField(_('Postal Code'), max_length=20)
    delivery_country = models.CharField(_('Country'), max_length=100, default='India')
    
    # Delivery preferences
    preferred_delivery_date = models.DateField(_('Preferred Delivery Date'))
    preferred_delivery_slot = models.CharField(_('Preferred Delivery Slot'), max_length=100)
    special_instructions = models.TextField(_('Special Instructions'), blank=True)
    
    # Gift options
    is_gift = models.BooleanField(_('Is Gift'), default=False)
    gift_message = models.TextField(_('Gift Message'), blank=True)
    
    # Tracking
    tracking_number = models.CharField(_('Tracking Number'), max_length=100, blank=True)
    shipped_date = models.DateTimeField(_('Shipped Date'), null=True, blank=True)
    delivered_date = models.DateTimeField(_('Delivered Date'), null=True, blank=True)
    
    # Metadata
    notes = models.TextField(_('Notes'), blank=True)
    payment_method = models.CharField(_('Payment Method'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        """Generate order number if not set."""
        if not self.order_number:
            # Generate a unique order number
            from datetime import datetime
            import random
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(random.randint(1000, 9999))
            self.order_number = f"NF{timestamp}{random_suffix}"
        super().save(*args, **kwargs)

    @property
    def grand_total(self):
        """Calculate grand total."""
        return self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount


class OrderItem(BaseModel):
    """
    Individual order item model.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('Quantity'))
    unit_price = models.DecimalField(_('Unit Price'), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_('Total Price'), max_digits=10, decimal_places=2)
    
    # Product details at time of order (in case product changes later)
    product_name = models.CharField(_('Product Name'), max_length=200)
    product_sku = models.CharField(_('Product SKU'), max_length=100)
    product_weight = models.CharField(_('Product Weight'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in order {self.order.order_number}"

    def save(self, *args, **kwargs):
        """Calculate total price before saving."""
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class ShippingMethod(BaseModel):
    """
    Shipping method model.
    """
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    estimated_delivery_days = models.PositiveIntegerField(_('Estimated Delivery Days'))
    is_available = models.BooleanField(_('Available'), default=True)
    min_order_amount = models.DecimalField(_('Minimum Order Amount'), max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _('Shipping Method')
        verbose_name_plural = _('Shipping Methods')

    def __str__(self):
        return self.name


class DeliverySlot(BaseModel):
    """
    Delivery slot model for scheduling.
    """
    day_of_week = models.CharField(_('Day of Week'), max_length=20)  # Monday, Tuesday, etc.
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    max_orders = models.PositiveIntegerField(_('Max Orders'), default=10)
    is_available = models.BooleanField(_('Available'), default=True)

    class Meta:
        verbose_name = _('Delivery Slot')
        verbose_name_plural = _('Delivery Slots')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.day_of_week} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class OrderStatusUpdate(BaseModel):
    """
    Track order status updates for timeline.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(_('Status'), max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    notes = models.TextField(_('Notes'), blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Order Status Update')
        verbose_name_plural = _('Order Status Updates')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order.order_number} - {self.status}"