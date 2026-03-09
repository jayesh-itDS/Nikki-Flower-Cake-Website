from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='list'),
    path('products/<slug:slug>/', views.product_detail, name='detail'),
    path('variant-price/<int:variant_id>/', views.get_variant_price, name='variant_price'),
]