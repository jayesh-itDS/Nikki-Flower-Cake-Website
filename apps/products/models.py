from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Category(BaseModel):
    """
    Product category model for organizing products.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name=_('Parent Category')
    )
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Occasion(BaseModel):
    """
    Occasion model for special events and celebrations.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    image = models.ImageField(upload_to='occasions/', null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=0)

    class Meta:
        verbose_name = _('Occasion')
        verbose_name_plural = _('Occasions')
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(BaseModel):
    """
    Main product model for flowers and cakes.
    """
    PRODUCT_TYPES = [
        ('flower', _('Flower')),
        ('cake', _('Cake')),
        ('combo', _('Combo')),
    ]

    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    description = models.TextField(_('Description'))
    short_description = models.CharField(_('Short Description'), max_length=300, blank=True)
    product_type = models.CharField(_('Product Type'), max_length=20, choices=PRODUCT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    occasions = models.ManyToManyField(Occasion, blank=True, related_name='products')
    
    # Pricing
    base_price = models.DecimalField(_('Base Price'), max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(_('Sale Price'), max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(_('Stock Quantity'), default=0)
    is_available = models.BooleanField(_('Available'), default=True)
    
    # Dimensions & Weight
    weight = models.CharField(_('Weight'), max_length=50, blank=True)  # e.g., "500g", "1kg"
    dimensions = models.CharField(_('Dimensions'), max_length=100, blank=True)  # e.g., "30x20x15 cm"
    
    # SEO & Marketing
    meta_title = models.CharField(_('Meta Title'), max_length=200, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=300, blank=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_trending = models.BooleanField(_('Trending'), default=False)
    
    # Image gallery
    primary_image = models.ImageField(_('Primary Image'), upload_to='products/')
    secondary_images = models.JSONField(_('Secondary Images'), default=list, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        """Return the sale price if available, otherwise the base price."""
        return self.sale_price if self.sale_price else self.base_price

    @property
    def is_on_sale(self):
        """Check if the product is on sale."""
        return self.sale_price is not None and self.sale_price < self.base_price

    @property
    def discount_percentage(self):
        """Calculate discount percentage if on sale."""
        if self.is_on_sale:
            return round(((self.base_price - self.sale_price) / self.base_price) * 100, 2)
        return 0

    def get_absolute_url(self):
        """Return the URL for the product detail page."""
        return reverse('products:detail', kwargs={'slug': self.slug})


class ProductVariant(BaseModel):
    """
    Product variant model for different sizes, flavors, etc.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(_('Name'), max_length=100)  # e.g., "Chocolate Flavor", "Medium Size"
    sku = models.CharField(_('SKU'), max_length=100, unique=True)
    price_modifier = models.DecimalField(_('Price Modifier'), max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(_('Stock Quantity'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        ordering = ['name']

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def final_price(self):
        """Calculate the final price with modifier."""
        return self.product.current_price + self.price_modifier


class ProductReview(BaseModel):
    """
    Product review model for user feedback.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(_('Rating'), choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(_('Title'), max_length=200)
    comment = models.TextField(_('Comment'))
    is_verified_purchase = models.BooleanField(_('Verified Purchase'), default=False)
    is_approved = models.BooleanField(_('Approved'), default=False)

    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating} stars)"


class ProductImage(models.Model):
    """
    Additional product images model.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['sort_order']

    def __str__(self):
        return f"Image for {self.product.name}"