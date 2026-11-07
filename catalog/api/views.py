from rest_framework import generics
from catalog.models import Category, Product
from .filters import ProductFilter
from .permissions import StaffWriteOtherwiseReadOnly
from .serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = (StaffWriteOtherwiseReadOnly,)
    filterset_class = ProductFilter
    search_fields = ("name", "description")
    ordering_fields = ("name", "unit_price", "inventory", "created_at")
    ordering = ("-created_at",)

    def get_serializer_class(self):
        return ProductDetailSerializer if self.request.method == "POST" else ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (StaffWriteOtherwiseReadOnly,)
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

