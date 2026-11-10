from rest_framework import serializers
from catalog.models import Product
from commerce.models import Basket, BasketItem, Order, OrderLine


class BasketItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.filter(is_active=True), write_only=True)
    product = serializers.CharField(source="product.name", read_only=True)
    unit_price = serializers.DecimalField(source="product.unit_price", max_digits=12, decimal_places=0, read_only=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=0, read_only=True)

    class Meta:
        model = BasketItem
        fields = ("id", "product_id", "product", "unit_price", "quantity", "subtotal")

    def validate(self, attrs):
        product = attrs.get("product") or self.instance.product
        quantity = attrs.get("quantity", self.instance.quantity if self.instance else 1)
        if quantity > product.inventory:
            raise serializers.ValidationError({"quantity": f"Only {product.inventory} unit(s) are available."})
        return attrs

    def create(self, validated_data):
        basket = self.context["basket"]
        product = validated_data["product"]
        quantity = validated_data["quantity"]
        item, created = BasketItem.objects.get_or_create(basket=basket, product=product, defaults={"quantity": quantity})
        if not created:
            new_quantity = item.quantity + quantity
            if new_quantity > product.inventory:
                raise serializers.ValidationError({"quantity": f"Only {product.inventory} unit(s) are available."})
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])
        return item


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=14, decimal_places=0, read_only=True)

    class Meta:
        model = Basket
        fields = ("id", "items", "total", "updated_at")


class OrderLineSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=0, read_only=True)

    class Meta:
        model = OrderLine
        fields = ("id", "product", "product_name", "unit_price", "quantity", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "status", "total_amount", "lines", "created_at", "updated_at")

