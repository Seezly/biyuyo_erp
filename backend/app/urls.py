"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from accounts.views.viewsets import UserViewSet, GroupViewSet
from accounts.views.auth import RegisterView, LoginView, LogoutView, MeView
from accounts.views.tokens import RefreshView
from billing.views import PlanViewSet, SubscriptionViewSet, InvoiceViewSet
from businesses.views import BusinessViewSet
from customers.views import CustomerViewSet
from inventory.views import CategoryViewSet, ProductViewSet, InventoryMovementViewSet
from sales.views import SaleViewSet, SaleItemViewSet, PaymentViewSet
from suppliers.views import SupplierViewSet, PurchaseViewSet, PurchaseItemViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"plans", PlanViewSet, basename="plans")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")
router.register(
    r"inventory-movements", InventoryMovementViewSet, basename="inventory-movements"
)
router.register(r"sales", SaleViewSet, basename="sales")
router.register(r"sale-items", SaleItemViewSet, basename="sale-items")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"suppliers", SupplierViewSet, basename="suppliers")
router.register(r"purchases", PurchaseViewSet, basename="purchases")
router.register(r"purchase-items", PurchaseItemViewSet, basename="purchase-items")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/refresh/", RefreshView.as_view(), name="token_refresh_cookie"),
    path("api/me/", MeView.as_view(), name="me"),
]
