from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sales-entry/', views.sales_entry, name='sales_entry'),
    path('inventory/', views.inventory, name='inventory'),
]
