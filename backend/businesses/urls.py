from django.urls import include, path
from rest_framework import routers

from businesses import views as businesses_views

router = routers.DefaultRouter()
router.register(r"businesses", businesses_views.BusinessViewSet, basename="business")

urlpatterns = [path("", include(router.urls))]
