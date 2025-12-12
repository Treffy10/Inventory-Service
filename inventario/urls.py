from django.urls import path
from .views import create_product, list_products, order_created_event

urlpatterns = [
    path("products/", create_product),
    path("products/all/", list_products),
    path("events/order-created/", order_created_event),
]
