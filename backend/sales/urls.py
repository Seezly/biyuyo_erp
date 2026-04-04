from django.urls import include, path
from rest_framework import routers

from sales import views as sales_views

router = routers.DefaultRouter()
router.register(r"sales", sales_views.SaleViewSet, basename="sale")
router.register(r"sale-items", sales_views.SaleItemViewSet, basename="sale_item")
router.register(r"payments", sales_views.PaymentViewSet, basename="payment")

urlpatterns = [path("", include(router.urls))]
