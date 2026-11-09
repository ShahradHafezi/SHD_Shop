from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from catalog.models import Product


class Basket(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="basket", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.select_related("product")), Decimal("0"))


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="basket_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["basket", "product"], name="unique_product_per_basket")]

    @property
    def subtotal(self):
        return self.product.unit_price * self.quantity

