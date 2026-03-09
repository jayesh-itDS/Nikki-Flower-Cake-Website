"""
URL configuration for Nikki Flower & Cake project.

Professional e-commerce platform URLs.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core apps
    path('', include('apps.products.urls', namespace='products')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('recommendations/', include('apps.recommendations.urls', namespace='recommendations')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('marketing/', include('apps.marketing.urls', namespace='marketing')),
    path('dashboard/', include('apps.admin_dashboard.urls', namespace='admin_dashboard')),
    
    # Static Pages
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
]

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
