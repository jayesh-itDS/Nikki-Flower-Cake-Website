from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.orders.models import Order


class Payment(BaseModel):
    """
    Payment model for handling payment transactions.
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
        ('cancelled', _('Cancelled')),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('razorpay', _('Razorpay')),
        ('credit_card', _('Credit Card')),
        ('debit_card', _('Debit Card')),
        ('net_banking', _('Net Banking')),
        ('upi', _('UPI')),
        ('wallet', _('Wallet')),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(_('Payment ID'), max_length=100, unique=True)
    payment_method = models.CharField(_('Payment Method'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(_('Status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=3, default='INR')
    gateway_response = models.JSONField(_('Gateway Response'), blank=True, null=True)
    captured = models.BooleanField(_('Captured'), default=False)
    captured_at = models.DateTimeField(_('Captured At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_number}"


class RazorpayWebhookLog(BaseModel):
    """
    Log Razorpay webhook events for debugging and reconciliation.
    """
    event_type = models.CharField(_('Event Type'), max_length=100)
    payload = models.JSONField(_('Payload'))
    processed = models.BooleanField(_('Processed'), default=False)
    processed_at = models.DateTimeField(_('Processed At'), null=True, blank=True)
    error_message = models.TextField(_('Error Message'), blank=True)

    class Meta:
        verbose_name = _('Razorpay Webhook Log')
        verbose_name_plural = _('Razorpay Webhook Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"