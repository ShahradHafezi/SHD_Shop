from django.db.models import Q
from django_filters import rest_framework as filters
from catalog.models import Product


class ProductFilter(filters.FilterSet):
    q = filters.CharFilter(method="search")
    category = filters.NumberFilter(field_name="category_id")
    category_slug = filters.CharFilter(field_name="category__slug")
    min_price = filters.NumberFilter(field_name="unit_price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="unit_price", lookup_expr="lte")
    in_stock = filters.BooleanFilter(method="filter_stock")

    class Meta:
        model = Product
        fields = ("q", "category", "category_slug", "min_price", "max_price", "in_stock")

    def search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def filter_stock(self, queryset, name, value):
        return queryset.filter(inventory__gt=0) if value else queryset.filter(inventory=0)

