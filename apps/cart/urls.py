from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/', views.add_to_cart, name='add'),
    path('remove/', views.remove_from_cart, name='remove'),
    path('update/', views.update_cart_item, name='update_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('process/', views.process_checkout, name='process'),
]