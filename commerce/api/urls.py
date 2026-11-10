from django.urls import path
from .views import BasketItemCreateView, BasketItemDetailView, BasketView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path("basket/", BasketView.as_view(), name="basket"),
    path("basket/items/", BasketItemCreateView.as_view(), name="basket-item-create"),
    path("basket/items/<int:pk>/", BasketItemDetailView.as_view(), name="basket-item-detail"),
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]

