from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class User(BaseModel, AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    USER_TYPES = [
        ('customer', _('Customer')),
        ('vendor', _('Vendor')),
        ('staff', _('Staff')),
        ('admin', _('Admin')),
    ]

    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    user_type = models.CharField(_('User Type'), max_length=20, choices=USER_TYPES, default='customer')
    profile_image = models.ImageField(_('Profile Image'), upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    is_email_verified = models.BooleanField(_('Email Verified'), default=False)
    is_phone_verified = models.BooleanField(_('Phone Verified'), default=False)
    newsletter_subscription = models.BooleanField(_('Newsletter Subscription'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email.split('@')[0]  # Use part before @ as name

    def get_display_name(self):
        """Return a display name for the user."""
        if self.first_name or self.last_name:
            return self.full_name
        else:
            return self.username or self.email.split('@')[0]


class UserProfile(BaseModel):
    """
    Extended user profile model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(_('Gender'), max_length=20, blank=True)
    anniversary_date = models.DateField(_('Anniversary Date'), null=True, blank=True)
    preferred_language = models.CharField(_('Preferred Language'), max_length=10, default='en')
    preferred_currency = models.CharField(_('Preferred Currency'), max_length=3, default='INR')
    shipping_address_same_as_billing = models.BooleanField(_('Shipping Same as Billing'), default=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile for {self.user.email}"


class UserWishlist(BaseModel):
    """
    User wishlist model for saving favorite products.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlists')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('User Wishlist')
        verbose_name_plural = _('User Wishlists')
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class UserAddress(BaseModel):
    """
    User address model for delivery addresses.
    """
    ADDRESS_TYPES = [
        ('home', _('Home')),
        ('work', _('Work')),
        ('other', _('Other')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    type = models.CharField(_('Type'), max_length=20, choices=ADDRESS_TYPES, default='home')
    full_name = models.CharField(_('Full Name'), max_length=200)
    phone_number = models.CharField(_('Phone Number'), max_length=15)
    street_address = models.CharField(_('Street Address'), max_length=255)
    landmark = models.CharField(_('Landmark'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20)
    country = models.CharField(_('Country'), max_length=100, default='India')
    is_default = models.BooleanField(_('Default Address'), default=False)

    class Meta:
        verbose_name = _('User Address')
        verbose_name_plural = _('User Addresses')

    def __str__(self):
        return f"{self.full_name} - {self.street_address}, {self.city}"


class UserActivityLog(BaseModel):
    """
    Log user activities for analytics and security.
    """
    ACTIVITY_TYPES = [
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('view_product', _('View Product')),
        ('add_to_cart', _('Add to Cart')),
        ('place_order', _('Place Order')),
        ('update_profile', _('Update Profile')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(_('Activity Type'), max_length=50, choices=ACTIVITY_TYPES)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    metadata = models.JSONField(_('Metadata'), default=dict, blank=True)

    class Meta:
        verbose_name = _('User Activity Log')
        verbose_name_plural = _('User Activity Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"