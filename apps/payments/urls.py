from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('demo/<int:order_id>/', views.payment_demo_view, name='demo'),
    path('process/<int:order_id>/', views.process_payment_view, name='process'),
]