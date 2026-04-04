from django.urls import include, path
from rest_framework import routers

from customers import views as customers_views

router = routers.DefaultRouter()
router.register(r"customers", customers_views.CustomerViewSet, basename="customer")

urlpatterns = [path("", include(router.urls))]
