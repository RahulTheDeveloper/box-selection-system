from decimal import Decimal

from django.test import TestCase

from boxes.models import Box
from boxes.services import (
    calculate_order_volume,
    calculate_order_weight,
    dimensions_fit,
    recommend_box,
)
from orders.models import Order, OrderItem
from products.models import Product

from rest_framework import status
from rest_framework.test import APITestCase

from django.core.cache import cache
from unittest.mock import patch


class BoxRecommendationServiceTests(TestCase):

    def setUp(self):
        self.small_box = Box.objects.create(
            name="Small Box",
            length=30,
            width=20,
            height=10,
            max_weight=5,
            cost=50,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            length=40,
            width=30,
            height=20,
            max_weight=10,
            cost=80,
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            length=60,
            width=40,
            height=30,
            max_weight=20,
            cost=120,
        )

        self.laptop = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=Decimal("2.5"),
        )

    def test_dimensions_fit_without_rotation(self):
        result = dimensions_fit(
            30,
            20,
            3,
            30,
            20,
            10,
        )

        self.assertTrue(result)

    def test_dimensions_fit_with_rotation(self):
        result = dimensions_fit(
            40,
            20,
            10,
            20,
            40,
            15,
        )

        self.assertTrue(result)

    def test_dimensions_do_not_fit(self):
        result = dimensions_fit(
            50,
            50,
            50,
            40,
            40,
            40,
        )

        self.assertFalse(result)

    def test_order_volume(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=2,
        )

        volume = calculate_order_volume(order)

        expected_volume = Decimal("3600")

        self.assertEqual(
            volume,
            expected_volume,
        )

    def test_order_weight(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=2,
        )

        weight = calculate_order_weight(order)

        expected_weight = Decimal("5.0")

        self.assertEqual(
            weight,
            expected_weight,
        )

    def test_recommends_smallest_suitable_box(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=1,
        )

        recommended_box = recommend_box(order)

        self.assertEqual(
            recommended_box,
            self.small_box,
        )

    def test_recommends_medium_box_when_small_box_weight_is_not_enough(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=3,
        )

        recommended_box = recommend_box(order)

        self.assertEqual(
            recommended_box,
            self.medium_box,
        )

    def test_returns_none_when_no_box_is_suitable(self):
        heavy_product = Product.objects.create(
            name="Heavy Product",
            length=20,
            width=20,
            height=10,
            weight=Decimal("50"),
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=heavy_product,
            quantity=1,
        )

        recommended_box = recommend_box(order)

        self.assertIsNone(recommended_box)

    def test_returns_none_for_empty_order(self):
        order = Order.objects.create()

        recommended_box = recommend_box(order)

        self.assertIsNone(recommended_box)

from rest_framework import status
from rest_framework.test import APITestCase


class RecommendationAPITests(APITestCase):

    def setUp(self):
        self.small_box = Box.objects.create(
            name="Small Box",
            length=30,
            width=20,
            height=10,
            max_weight=5,
            cost=50,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            length=40,
            width=30,
            height=20,
            max_weight=10,
            cost=80,
        )

        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2.5,
        )

        self.order = Order.objects.create()

    def test_recommend_box_for_order(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

        response = self.client.post(
            f"/api/boxes/recommend/{self.order.id}/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["recommended_box"]["id"],
            self.small_box.id,
        )

    def test_recommend_medium_box_when_small_box_weight_is_not_enough(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
        )

        response = self.client.post(
            f"/api/boxes/recommend/{self.order.id}/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["recommended_box"]["id"],
            self.medium_box.id,
        )

    def test_recommendation_for_empty_order(self):
        response = self.client.post(
            f"/api/boxes/recommend/{self.order.id}/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_recommendation_for_non_existing_order(self):
        response = self.client.post(
            "/api/boxes/recommend/99999/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_no_suitable_box(self):
        heavy_product = Product.objects.create(
            name="Heavy Product",
            length=20,
            width=20,
            height=10,
            weight=50,
        )

        OrderItem.objects.create(
            order=self.order,
            product=heavy_product,
            quantity=1,
        )

        response = self.client.post(
            f"/api/boxes/recommend/{self.order.id}/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

class RecommendationCacheTests(APITestCase):

    def setUp(self):
        cache.clear()

        self.box = Box.objects.create(
            name="Small Box",
            length=30,
            width=20,
            height=10,
            max_weight=5,
            cost=50,
        )

        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2.5,
        )

        self.order = Order.objects.create()

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

    def tearDown(self):
        cache.clear()

    def test_recommendation_is_cached(self):
        url = f"/api/boxes/recommend/{self.order.id}/"

        response = self.client.post(
            url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        cache_key = (
            f"order_recommendation:{self.order.id}"
        )

        cached_data = cache.get(cache_key)

        self.assertIsNotNone(cached_data)

        self.assertEqual(
            cached_data["order_id"],
            self.order.id,
        )

        self.assertEqual(
            cached_data["recommended_box"]["id"],
            self.box.id,
        )

    def test_second_request_uses_cache(self):
        url = f"/api/boxes/recommend/{self.order.id}/"

        # First request creates the cache.
        first_response = self.client.post(
            url,
            {},
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK,
        )

        # Second request should use cached result.
        with patch(
            "boxes.views.recommend_box"
        ) as mock_recommend_box:

            second_response = self.client.post(
                url,
                {},
                format="json",
            )

            self.assertEqual(
                second_response.status_code,
                status.HTTP_200_OK,
            )

            mock_recommend_box.assert_not_called()

        self.assertEqual(
            second_response.data,
            first_response.data,
        )                