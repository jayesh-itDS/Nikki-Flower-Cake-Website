from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.users.models import User
from apps.products.models import Product, ProductVariant


class Cart(BaseModel):
    """
    Main shopping cart model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(_('Session Key'), max_length=40, null=True, blank=True)
    coupon_code = models.CharField(_('Coupon Code'), max_length=50, blank=True)
    notes = models.TextField(_('Special Instructions'), blank=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        else:
            return f"Guest Cart - {self.session_key}"

    @property
    def total_items(self):
        """Total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Subtotal before discounts."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_discount(self):
        """Total discount amount."""
        # Placeholder - implement coupon logic
        return 0

    @property
    def total(self):
        """Final total after discounts."""
        return self.subtotal - self.total_discount


class CartItem(BaseModel):
    """
    Individual cart item model.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    unit_price = models.DecimalField(_('Unit Price'), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_('Total Price'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

    def save(self, *args, **kwargs):
        """Calculate total price before saving."""
        if self.variant:
            self.unit_price = self.variant.final_price
        else:
            self.unit_price = self.product.current_price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def update_quantity(self, new_quantity):
        """Update item quantity."""
        self.quantity = new_quantity
        self.save()


class Wishlist(BaseModel):
    """
    User wishlist model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by_cart')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cart Wishlist')
        verbose_name_plural = _('Cart Wishlists')
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class Coupon(BaseModel):
    """
    Coupon/discount code model.
    """
    DISCOUNT_TYPES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]

    code = models.CharField(_('Code'), max_length=50, unique=True)
    discount_type = models.CharField(_('Discount Type'), max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(_('Discount Value'), max_digits=10, decimal_places=2)
    minimum_order_value = models.DecimalField(_('Minimum Order Value'), max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(_('Usage Limit'), null=True, blank=True)
    used_count = models.PositiveIntegerField(_('Used Count'), default=0)
    valid_from = models.DateTimeField(_('Valid From'))
    valid_until = models.DateTimeField(_('Valid Until'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        """Check if coupon is currently valid."""
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_until and
                (self.usage_limit is None or self.used_count < self.usage_limit))

    def can_be_applied(self, order_total):
        """Check if coupon can be applied to an order."""
        if not self.is_valid:
            return False
        if self.minimum_order_value and order_total < self.minimum_order_value:
            return False
        return True

    def calculate_discount(self, order_total):
        """Calculate discount amount for an order."""
        if not self.can_be_applied(order_total):
            return 0
        
        if self.discount_type == 'percentage':
            discount_amount = (self.discount_value / 100) * order_total
            # Cap at order total to prevent negative total
            return min(discount_amount, order_total)
        elif self.discount_type == 'fixed':
            # Cap at order total to prevent negative total
            return min(self.discount_value, order_total)
        return 0