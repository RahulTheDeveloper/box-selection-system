from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Box
from .serializers import BoxSerializer
from .services import recommend_box
from django.core.cache import cache

from orders.models import Order


class BoxListCreateView(APIView):

    def get(self, request):
        boxes = Box.objects.all()
        serializer = BoxSerializer(boxes, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = BoxSerializer(data=request.data)

        if serializer.is_valid():
            box = serializer.save()

            return Response(
                BoxSerializer(box).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BoxDetailView(APIView):

    def get_object(self, pk):
        try:
            return Box.objects.get(pk=pk)

        except Box.DoesNotExist:
            return None

    def get(self, request, pk):
        box = self.get_object(pk)

        if box is None:
            return Response(
                {"detail": "Box not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BoxSerializer(box)

        return Response(serializer.data)

    def put(self, request, pk):
        box = self.get_object(pk)

        if box is None:
            return Response(
                {"detail": "Box not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BoxSerializer(
            box,
            data=request.data
        )

        if serializer.is_valid():
            box = serializer.save()

            return Response(
                BoxSerializer(box).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        box = self.get_object(pk)

        if box is None:
            return Response(
                {"detail": "Box not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BoxSerializer(
            box,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            box = serializer.save()

            return Response(
                BoxSerializer(box).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        box = self.get_object(pk)

        if box is None:
            return Response(
                {"detail": "Box not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        box.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class RecommendationView(APIView):

    CACHE_TIMEOUT = 300

    def post(self, request, order_id):

        try:
            order = Order.objects.prefetch_related(
                "items__product"
            ).get(pk=order_id)

        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not order.items.exists():
            return Response(
                {"detail": "Order has no items."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f"order_recommendation:{order_id}"

        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return Response(
                cached_result,
                status=status.HTTP_200_OK
            )

        recommended_box = recommend_box(order)

        if recommended_box is None:
            return Response(
                {
                    "detail": (
                        "No suitable box found for this order."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = {
            "order_id": order.id,
            "recommended_box": BoxSerializer(
                recommended_box
            ).data,
        }

        cache.set(
            cache_key,
            response_data,
            self.CACHE_TIMEOUT
        )

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )