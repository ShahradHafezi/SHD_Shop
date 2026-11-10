from django.db import transaction
from rest_framework.exceptions import ValidationError
from catalog.models import Product
from commerce.models import Basket, Order, OrderLine


@transaction.atomic
def checkout_basket(user):
    basket = Basket.objects.filter(user=user).first()
    if not basket or not basket.items.exists():
        raise ValidationError({"basket": "Basket is empty."})

    items = list(basket.items.all())
    prepared_items = []
    total = 0

    for item in items:
        product = Product.objects.select_for_update().get(pk=item.product_id)
        if not product.is_active or item.quantity > product.inventory:
            raise ValidationError({"basket": f"Insufficient inventory for {product.name}."})
        prepared_items.append((item, product))
        total += product.unit_price * item.quantity

    order = Order.objects.create(user=user, total_amount=total)
    for item, product in prepared_items:
        product.inventory -= item.quantity
        product.save(update_fields=["inventory"])
        OrderLine.objects.create(
            order=order, product=product, product_name=product.name,
            unit_price=product.unit_price, quantity=item.quantity,
        )

    basket.items.all().delete()
    return order


@transaction.atomic
def release_reserved_stock(order):
    if order.status != Order.Status.PENDING:
        return

    for line in order.lines.select_related("product"):
        product = Product.objects.select_for_update().get(pk=line.product_id)
        product.inventory += line.quantity
        product.save(update_fields=["inventory"])

