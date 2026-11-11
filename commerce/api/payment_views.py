from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from commerce.models import Order, Payment
from commerce.services import release_reserved_stock
from commerce.zarinpal import request_payment, verify_payment


class PaymentRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != Order.Status.PENDING:
            return Response({"detail": "Order is not pending."}, status=status.HTTP_400_BAD_REQUEST)

        amount = int(order.total_amount * 10)
        try:
            authority, payment_url = request_payment(amount, order.pk)
        except Exception as error:
            return Response({"detail": str(error)}, status=status.HTTP_502_BAD_GATEWAY)

        Payment.objects.create(order=order, authority=authority, amount_rial=amount)
        return Response({"payment_url": payment_url}, status=status.HTTP_201_CREATED)


class PaymentVerifyView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        authority = request.query_params.get("Authority")
        payment = get_object_or_404(Payment.objects.select_related("order"), authority=authority)
        order = payment.order

        if request.query_params.get("Status") != "OK":
            release_reserved_stock(order)
            order.status = Order.Status.FAILED
            order.save()
            payment.status = Payment.Status.FAILED
            payment.save()
            return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reference_id = verify_payment(authority, payment.amount_rial)
        except Exception as error:
            return Response({"detail": str(error)}, status=status.HTTP_502_BAD_GATEWAY)

        payment.status = Payment.Status.VERIFIED
        payment.reference_id = reference_id
        payment.verified_at = timezone.now()
        payment.save()
        order.status = Order.Status.PAID
        order.save()
        return Response({"status": "paid", "reference_id": reference_id})

