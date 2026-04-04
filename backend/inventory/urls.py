from django.urls import include, path
from rest_framework import routers

from inventory import views as inventory_views

router = routers.DefaultRouter()
router.register(r"products", inventory_views.ProductViewSet, basename="product")
router.register(r"categories", inventory_views.CategoryViewSet, basename="category")
router.register(r"inventory-movements", inventory_views.InventoryMovementViewSet, basename="inventory_movement")

urlpatterns = [path("", include(router.urls))]
