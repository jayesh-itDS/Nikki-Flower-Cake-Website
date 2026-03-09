from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product, Occasion
from apps.core.models import BaseModel


class ProductEvent(BaseModel):
    """
    Track user interactions with products for recommendation engine.
    """
    class EventType(models.TextChoices):
        VIEW = "view", "View"
        ADD_TO_CART = "add_to_cart", "Add to cart"
        PURCHASE = "purchase", "Purchase"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='product_events'
    )
    session_key = models.CharField(max_length=40, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    occasion = models.ForeignKey(
        Occasion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='product_events'
    )

    class Meta:
        verbose_name = _('Product Event')
        verbose_name_plural = _('Product Events')
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.event_type} - {self.product.name}"


class ProductRecommendation(BaseModel):
    """
    Pre-computed product recommendations.
    """
    base_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="recommendations_from",
    )
    recommended_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="recommended_for",
    )
    score = models.FloatField(default=0, help_text=_('Recommendation score (higher is better)'))
    reason = models.CharField(max_length=40, blank=True, help_text=_('Reason for recommendation, e.g. "also_bought"'))

    class Meta:
        verbose_name = _('Product Recommendation')
        verbose_name_plural = _('Product Recommendations')
        unique_together = ("base_product", "recommended_product", "reason")

    def __str__(self):
        return f"{self.base_product.name} -> {self.recommended_product.name}"

