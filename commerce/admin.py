from django.contrib import admin
from .models import Basket, BasketItem, Order, OrderLine

admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)
admin.site.register(OrderLine)

