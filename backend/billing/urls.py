from django.urls import include, path
from rest_framework import routers

from billing import views as billing_views

router = routers.DefaultRouter()
router.register(r"plans", billing_views.PlanViewSet, basename="plan")
router.register(r"subscriptions", billing_views.SubscriptionViewSet, basename="subscription")
router.register(r"invoices", billing_views.InvoiceViewSet, basename="invoice")

urlpatterns = [path("", include(router.urls))]
