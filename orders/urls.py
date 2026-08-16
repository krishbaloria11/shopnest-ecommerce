from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='confirmation'),
    path('history/', views.order_history, name='history'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('detail/<int:order_id>/', views.order_detail, name='detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel'),
]

