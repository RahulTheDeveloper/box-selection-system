from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITests(APITestCase):

    def setUp(self):
        self.product_data = {
            "name": "Laptop",
            "length": 30,
            "width": 20,
            "height": 3,
            "weight": 2.5,
        }

    def test_create_product(self):
        response = self.client.post(
            "/api/products/",
            self.product_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Laptop",
        )

        self.assertEqual(
            Decimal(response.data["weight"]),
            Decimal("2.5"),
        )

    def test_get_all_products(self):
        Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2.5,
        )

        response = self.client.get(
            "/api/products/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_get_product_by_id(self):
        product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2.5,
        )

        response = self.client.get(
            f"/api/products/{product.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            product.id,
        )

    def test_create_product_with_invalid_dimensions(self):
        invalid_data = {
            "name": "Invalid Product",
            "length": -30,
            "width": 20,
            "height": 3,
            "weight": 2.5,
        }

        response = self.client.post(
            "/api/products/",
            invalid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_get_non_existing_product(self):
        response = self.client.get(
            "/api/products/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )