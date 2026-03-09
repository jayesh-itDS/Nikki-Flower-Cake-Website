from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    """
    Abstract model for adding created_at and updated_at timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Abstract model for soft deletion functionality.
    """
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseModel(TimestampMixin, SoftDeleteMixin):
    """
    Base model combining timestamp and soft delete functionality.
    """
    class Meta:
        abstract = True


class Address(models.Model):
    """
    Reusable address model for users and orders.
    """
    ADDRESS_TYPES = [
        ('home', _('Home')),
        ('work', _('Work')),
        ('other', _('Other')),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f"{self.full_name} - {self.street_address}, {self.city}"


class Notification(models.Model):
    """
    System notification model for user communications.
    """
    NOTIFICATION_TYPES = [
        ('order', _('Order Updates')),
        ('promotion', _('Promotions')),
        ('general', _('General')),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"