from django.urls import include, path
from rest_framework import routers

from suppliers import views as suppliers_views

router = routers.DefaultRouter()
router.register(r"suppliers", suppliers_views.SupplierViewSet, basename="supplier")
router.register(r"purchase-orders", suppliers_views.PurchaseViewSet, basename="purchase_order")
router.register(r"purchase-items", suppliers_views.PurchaseItemViewSet, basename="purchase_item")

urlpatterns = [path("", include(router.urls))]
