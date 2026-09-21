from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from django.core.cache import cache







class OrderListCreateView(APIView):

    def get(self, request):
        orders = Order.objects.all().prefetch_related(
            "items"
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(
            data=request.data
        )

        if serializer.is_valid():
            order = serializer.save()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderDetailView(APIView):

    def get_object(self, pk):
        try:
            return Order.objects.prefetch_related(
                "items"
            ).get(pk=pk)

        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)

        if order is None:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)

        return Response(serializer.data)

    def delete(self, request, pk):
        order = self.get_object(pk)

        if order is None:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        order.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class OrderItemCreateView(APIView):

    def post(self, request, order_id):

        try:
            order = Order.objects.get(pk=order_id)

        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderItemSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        existing_item = OrderItem.objects.filter(
            order=order,
            product=product
        ).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()

            cache.delete(
                f"order_recommendation:{order_id}"
            )

            return Response(
                OrderItemSerializer(existing_item).data,
                status=status.HTTP_200_OK
            )

        order_item = serializer.save(
            order=order
        )

        cache.delete(
            f"order_recommendation:{order_id}"
        )

        return Response(
            OrderItemSerializer(order_item).data,
            status=status.HTTP_201_CREATED
        )