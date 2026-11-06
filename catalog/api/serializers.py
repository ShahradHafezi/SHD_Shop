from rest_framework import serializers
from catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "description")


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "unit_price", "inventory", "category")


class ProductDetailSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "unit_price", "inventory",
            "is_active", "category", "category_title", "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

