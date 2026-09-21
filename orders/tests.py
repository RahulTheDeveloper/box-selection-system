from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from orders.models import Order, OrderItem


class OrderAPITests(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=3,
            weight=2.5,
        )

        self.order = Order.objects.create()

    def test_create_order(self):
        response = self.client.post(
            "/api/orders/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertIn(
            "id",
            response.data,
        )

    def test_get_all_orders(self):
        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_get_order_by_id(self):
        response = self.client.get(
            f"/api/orders/{self.order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.order.id,
        )

    def test_add_product_to_order(self):
        response = self.client.post(
            f"/api/orders/{self.order.id}/items/",
            {
                "product": self.product.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["product"],
            self.product.id,
        )

        self.assertEqual(
            response.data["quantity"],
            2,
        )

    def test_invalid_quantity(self):
        response = self.client.post(
            f"/api/orders/{self.order.id}/items/",
            {
                "product": self.product.id,
                "quantity": 0,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_non_existing_order(self):
        response = self.client.post(
            "/api/orders/99999/items/",
            {
                "product": self.product.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_duplicate_product_updates_quantity(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )

        response = self.client.post(
            f"/api/orders/{self.order.id}/items/",
            {
                "product": self.product.id,
                "quantity": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["quantity"],
            5,
        )

    def test_get_order_contains_items(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )

        response = self.client.get(
            f"/api/orders/{self.order.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

        self.assertEqual(
            response.data["items"][0]["quantity"],
            2,
        )