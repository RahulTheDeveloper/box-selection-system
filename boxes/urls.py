from django.urls import path

from .views import (
    BoxListCreateView,
    BoxDetailView,
    RecommendationView,
)


urlpatterns = [
    path("",BoxListCreateView.as_view(),name="box-list-create",),
    path("<int:pk>/",BoxDetailView.as_view(),name="box-detail",),
    path("recommend/<int:order_id>/",RecommendationView.as_view(),name="box-recommendation"),
]