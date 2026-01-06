# payments/urls.py

from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('', views.payment_list_view, name='payment_list'),
    path('new/', views.payment_create_view, name='payment_create'),
    # Detal, tahrirlash va o'chirish keyingi qadamlarda qo'shilishi mumkin
    # path('<int:pk>/', views.payment_detail_view, name='payment_detail'),
]