from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    OrderItemCreateView,
)


urlpatterns = [
    path("",OrderListCreateView.as_view(),name="order-list-create",),
    path("<int:pk>/", OrderDetailView.as_view(),name="order-detail",),
    path("<int:order_id>/items/",OrderItemCreateView.as_view(),name="Order-Item-create"),
]