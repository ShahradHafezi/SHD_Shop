from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from commerce.models import Basket, BasketItem
from .serializers import BasketItemSerializer, BasketSerializer


def current_basket(user):
    return Basket.objects.get_or_create(user=user)[0]


class BasketView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(BasketSerializer(current_basket(request.user)).data)

    def delete(self, request):
        current_basket(request.user).items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BasketItemCreateView(generics.CreateAPIView):
    serializer_class = BasketItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["basket"] = current_basket(self.request.user)
        return context


class BasketItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = BasketItemSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ("patch", "delete", "options")

    def get_queryset(self):
        return BasketItem.objects.filter(basket__user=self.request.user).select_related("product")

