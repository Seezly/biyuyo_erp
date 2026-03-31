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

from accounts import views as accounts_views
from billing import views as billing_views
from businesses import views as businesses_views
from customers import views as customers_views
from inventory import views as inventory_views
from sales import views as sales_views
from suppliers import views as suppliers_views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()

# Register accounts app viewsets with the router
router.register(r"users", accounts_views.UserViewSet)
router.register(r"groups", accounts_views.GroupViewSet)

# Register billing app viewsets with the router
router.register(r"plans", billing_views.PlanViewSet)
router.register(r"subscriptions", billing_views.SubscriptionViewSet)
router.register(r"invoices", billing_views.InvoiceViewSet)

# Register businesses app viewsets with the router
router.register(r"businesses", businesses_views.BusinessViewSet)

# Register customers app viewsets with the router
router.register(r"customers", customers_views.CustomerViewSet)

# Register inventory app viewsets with the router
router.register(r"products", inventory_views.ProductViewSet)
router.register(r"categories", inventory_views.CategoryViewSet)
router.register(r"inventory-movements", inventory_views.InventoryMovementViewSet)

# Register sales app viewsets with the router
router.register(r"sales", sales_views.SaleViewSet)
router.register(r"sale-items", sales_views.SaleItemViewSet)
router.register(r"payments", sales_views.PaymentViewSet)

# Register suppliers app viewsets with the router
router.register(r"suppliers", suppliers_views.SupplierViewSet)
router.register(r"purchase-orders", suppliers_views.PurchaseViewSet)
router.register(r"purchase-items", suppliers_views.PurchaseItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
